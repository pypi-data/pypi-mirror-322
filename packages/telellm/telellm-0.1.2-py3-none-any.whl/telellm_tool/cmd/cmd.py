# Copyright 2024 State Cloud.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""cmd"""
import os
import shutil
import sys
from datetime import datetime
import multiprocessing
import click
from jinja2 import Template
import telellm_tool
from telellm_tool.utils.markdown_utils import MarkdownTableManager



def exit_process(err):
    """
    Prints the error message and terminates the program with a non-zero exit status.
    """
    click.echo(err)
    sys.exit(1)


def render_template(template_path, **kwargs):
    """
    Renders a template from the specified file with provided arguments and overwrites the file with the rendered output.
    """
    with open(template_path, "r", encoding="utf-8") as file:
        template = Template(file.read())
    output = template.render(**kwargs)
    with open(template_path, "w", encoding="utf-8") as file:
        file.write(output)


def version_cmd():
    """
    Outputs the current version of the tool.
    """
    click.echo(telellm_tool.version)


def test_report_cmd(test_type, service_host, service_port, service_name, model_name, concurrency, seq_len):
    """
    Generates and renders both functional and performance test reports based on the provided test type.
    """
    from telellm_tool.cmd.test_cmd.test_function import verify_error_code, test_regular_qa
    from telellm_tool.cmd.test_cmd.test_performance import get_inference_info
    cur_path = os.getcwd()
    click.echo(cur_path)

    report_template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_cmd"))
    click.echo(report_template_path)

    current_time = datetime.now().strftime("%Y.%m.%d")

    if test_type in ['functional', 'both']:
        src_functional_report = "LLM-InferService-FunctionalTest-Report.md"
        src_file = os.path.join(report_template_path, src_functional_report)
        dst_functional_report = f"LLM-{service_name}-{model_name}-功能测试报告.md"
        dst_file = os.path.join(cur_path, dst_functional_report)
        shutil.copyfile(src_file, dst_file)

        # 常规问答测试
        click.echo("perform regular_qa_test")
        regular_qa_result = test_regular_qa(service_host, service_port, model_name)

        # 错误码校验
        # click.echo("perform error_code_verify")
        # error_code_result = verify_error_code(service_host, service_port, model_name)
        error_code_result = None

        # render 功能测试报告
        render_template(dst_file, SERVICE_NAME=service_name, MODEL_NAME=model_name, CURRENT_TIME=current_time,
                        REGULAR_QA_RESULT=regular_qa_result, ERROR_CODE_RESULT=error_code_result)
        click.echo("render functional_test_report success")

    if test_type in ['performance', 'both']:
        src_performance_report = "LLM-InferService-PerformanceTest-Report.md"
        src_file = os.path.join(report_template_path, src_performance_report)
        dst_performance_report = f"LLM-{service_name}-{model_name}-性能测试报告.md"
        dst_file = os.path.join(cur_path, dst_performance_report)
        shutil.copyfile(src_file, dst_file)

        # 性能测试
        click.echo("perform performance test")
        performance_report_table = get_inference_info(service_host, service_port, model_name, concurrency, seq_len)

        # render 性能测试报告
        render_template(dst_file, SERVICE_NAME=service_name, MODEL_NAME=model_name,
                        CURRENT_TIME=current_time, PERFORMANCE_RESULT=performance_report_table)
        click.echo("render performance_test_report success")


def eval_cmd(service_host, service_port, model_name, dataset, _type, overwrite, num_threads, request_param):
    """
    Evaluates the model on specified datasets (MMLU, C-Eval, HumanEval, GSM8K) and generates a report in Markdown format.
    """
    from telellm_tool.cmd.eval_cmd.evaluate_chat_ceval import eval_chat_ceval
    from telellm_tool.cmd.eval_cmd.evaluate_chat_gsm8k import eval_chat_gsm8k
    from telellm_tool.cmd.eval_cmd.evaluate_chat_humaneval import eval_chat_humaneval
    from telellm_tool.cmd.eval_cmd.evaluate_chat_mmlu import eval_chat_mmlu
    cur_path = os.getcwd()
    click.echo(cur_path)
    eval_report_md_path = os.path.join(cur_path, f"{model_name}_eval_report.md")
    click.echo(eval_report_md_path)

    # MarkdownTableManager
    manager = MarkdownTableManager(eval_report_md_path)
    table_name = ""
    table_dict = {}

    if dataset == "mmlu":
        table_name = f"MMLU({_type})"
        table_dict = eval_chat_mmlu(service_host, service_port, model_name, _type, overwrite,
                                    num_threads, request_param)
    elif dataset == "ceval":
        table_name = f"C-Eval({_type})"
        table_dict = eval_chat_ceval(service_host, service_port, model_name, _type, overwrite,
                                     num_threads, request_param)
    elif dataset == "humaneval":
        table_name = "HumanEval"
        table_dict = eval_chat_humaneval(service_host, service_port, model_name, _type, overwrite,
                                         num_threads, request_param)
    elif dataset == "gsm8k":
        table_name = "GSM8K"
        table_dict = eval_chat_gsm8k(service_host, service_port, model_name, _type, overwrite,
                                     num_threads, request_param)

    # tables -> file save
    if table_dict is not None:
        table = manager.get_table(table_name, overwrite=True)
        table.add_columns_from_dict(table_dict)
        manager.save_to_file()
        click.echo(f"{eval_report_md_path} generate success")


def quantify_cmd(kwargs):
    """
    Performs model quantization, evaluates performance and accuracy, and generates a quantization report.
    """
    from telellm_tool.cmd.quant_cmd.quant_utils import check_json_config, load_config, save_result
    from telellm_tool.cmd.quant_cmd.benchmark_run import performance_sync_forward, accuracy_sync_forward
    from telellm_tool.cmd.quant_cmd.quantify import start_quant_llm
    # 检查参数，有些是必传的
    use_json = check_json_config(kwargs.get('config_path'))
    # 优选使用json配置文件，否则检验必传参数
    if not use_json and (
            kwargs.get('model_path').strip() in [None, ""] or kwargs.get('save_directory').strip() in [None, ""]):
        raise ValueError("model_path and save_directory are required")
    # 获取所有的参数
    config = load_config(kwargs, use_json)
    # 量化大模型 华为的量化程序在结束后未释放内存
    p = multiprocessing.Process(target=start_quant_llm, args=(config,))
    p.start()
    p.join()
    # 性能测试比对
    is_performance = config.performance
    origin_model_performance = {}
    quant_model_performance = {}
    # 为什么用进程？ 因为华为共享了config路径，需要用进程隔离才能加载不同的config
    if is_performance:
        queue = multiprocessing.Queue()
        process_1 = multiprocessing.Process(target=performance_sync_forward, args=(config.model_path, queue))
        process_2 = multiprocessing.Process(target=performance_sync_forward, args=(config.save_directory, queue))
        # 启动第一个进程
        process_1.start()
        process_1.join()  # 等待第一个进程完成

        # 启动第二个进程
        process_2.start()
        process_2.join()  # 等待第二个进程完成
        origin_model_performance = queue.get()
        quant_model_performance = queue.get()
    # 精度测试对比
    is_accuracy = config.accuracy
    origin_model_accuracy = {}
    quant_model_accuracy = {}
    if is_accuracy:
        queue = multiprocessing.Queue()
        process_1 = multiprocessing.Process(target=accuracy_sync_forward, args=(
            config.dataset, config.model_path, config.type, config.num_threads, queue))
        process_2 = multiprocessing.Process(target=accuracy_sync_forward, args=(
            config.dataset, config.save_directory, config.type, config.num_threads, queue))
        # 启动第一个进程
        process_1.start()
        process_1.join()  # 等待第一个进程完成

        # 启动第二个进程
        process_2.start()
        process_2.join()  # 等待第二个进程完成
        origin_model_accuracy = queue.get()
        quant_model_accuracy = queue.get()
    # 生成量化报告
    save_result(origin_model_performance, quant_model_performance, origin_model_accuracy, quant_model_accuracy, config)


def gen_quant_config():
    """
    Generates quantization configuration and calibration files in the current directory.
    """
    from telellm_tool.cmd.quant_cmd.quant_utils import check_json_config, load_config, save_result
    from telellm_tool.cmd.quant_cmd.benchmark_run import performance_sync_forward, accuracy_sync_forward
    from telellm_tool.cmd.quant_cmd.quantify import start_quant_llm
    cur_path = os.getcwd()
    user_path = os.path.join(cur_path, 'quant_config.json')
    template_path = os.path.join(os.path.dirname(__file__), 'quant_cmd', 'quant_config.json')

    # 先删除已存在的user_path文件
    if os.path.exists(user_path):
        os.remove(user_path)
    # 复制template_path到user_path
    shutil.copyfile(template_path, user_path)

    user_path = os.path.join(cur_path, 'calib.jsonl')
    template_path = os.path.join(os.path.dirname(__file__), 'quant_cmd', 'calib.jsonl')

    if os.path.exists(user_path):
        os.remove(user_path)
    shutil.copyfile(template_path, user_path)
    click.echo("quant config json and calib file has been generated to the current directory")


# 测试接口
def perform_test(performance, accuracy, dataset="mmlu", _type="val", num_threads=5):
    """
    Performs performance and accuracy tests on models based on provided configuration.
    """
    from telellm_tool.cmd.quant_cmd.benchmark_run import performance_sync_forward, accuracy_sync_forward
    if performance:
        queue = multiprocessing.Queue()
        process_1 = multiprocessing.Process(target=performance_sync_forward, args=("/model/Llama-2-7b-chat-hf", queue))
        process_2 = multiprocessing.Process(target=performance_sync_forward,
                                            args=("/model/Llama-2-7b-chat-hf-w8a8-disable", queue))
        # 启动第一个进程
        process_1.start()
        process_1.join()  # 等待第一个进程完成

        # 启动第二个进程
        process_2.start()
        process_2.join()  # 等待第二个进程完成
        origin_model_performance = queue.get()
        quant_model_performance = queue.get()
        # origin_model_performance = performance_sync_forward(model_path="/model/Qwen2-72B-Instruct")
        # quant_model_performance = performance_sync_forward(model_path="/model/Qwen2-72B-Instruct-w8a8-disable")
        print(origin_model_performance)
        print(quant_model_performance)
        # speed_up = round(quant_model_performance[2] / origin_model_performance[2], 2)
        # print(speed_up)
    if accuracy:
        model_path = "/model/Qwen2-72B-Instruct"
        print(accuracy_sync_forward(dataset, model_path, _type, num_threads, None))


def serve_cmd(model, service_name, port, model_precision, tensor_parallel_size, topk, temperature, topp,
          repetition_penalty, model_name, max_num_seq, max_length, gpu_memory_utilization, max_num_batched_tokens):
    """
    Configures and starts the service with the provided model and hyperparameters.
    """
    
    from telellm_tool.cmd.service import start_service
    from telellm.config.config import CFG
    print("*****my_config_list*****")
    print("model:", model)
    print("service_name:", service_name)
    print("port:", port)
    print("model_precision:", model_precision)
    print("tensor_parallel_size:", tensor_parallel_size)
    print("topk:", topk)
    print("temperature:", temperature)
    print("topp:", topp)
    print("repetition_penalty:", repetition_penalty)
    print("model_name:", model_name)
    print("max_num_seq:", max_num_seq)
    print("max_length:", max_length)
    print("gpu_memory_utilization:", gpu_memory_utilization)
    print("max_num_batched_tokens:", max_num_batched_tokens)
    print("*****End*****")
    CFG["LLM"]["MODEL_PATH"] = model
    CFG["SERVICE"]["NAME"] = service_name
    CFG["SERVICE"]["PORT"] = int(port)
    CFG["LLM"]["MODEL_PRECISION"] = model_precision
    CFG["LLM"]["TENSOR_PARALLEL_SIZE"] = int(tensor_parallel_size)
    CFG["LLM"]["DEFAULT_TOPK"] = int(topk)
    CFG["LLM"]["DEFAULT_TEMPERATURE"] = float(temperature)
    CFG["LLM"]["DEFAULT_TOPP"] = float(topp)
    CFG["LLM"]["DEFAULT_REPETITION_PENALTY"] = float(repetition_penalty)
    CFG["LLM"]["MODEL_NAME"] = model_name
    CFG["LLM"]["DEFAULT_MAX_NUM_SEQS"] = int(max_num_seq)
    CFG["LLM"]["DEFAULT_MAX_LENGTH"] = int(max_length)
    CFG["LLM"]["DEFAULT_GPU_MEMORY_UTILIZATION"] = float(gpu_memory_utilization)
    if not max_num_batched_tokens:
        CFG["LLM"]["DEFAULT_MAX_NUM_BATCHED_TOKENS"] = int(max_length)
    else:
        CFG["LLM"]["DEFAULT_MAX_NUM_BATCHED_TOKENS"] = int(max_num_batched_tokens)
    start_service()
    