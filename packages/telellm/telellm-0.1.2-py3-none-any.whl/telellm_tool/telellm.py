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
"""telellm"""
import click
from telellm_tool.cmd.cmd import version_cmd, test_report_cmd, eval_cmd, quantify_cmd, \
    gen_quant_config, perform_test, serve_cmd
from telellm_tool.const.click_setting import CONTEXT_SETTINGS


@click.group()
def cli():
    """cli"""
    pass


# 版本信息
@cli.command('version', short_help='get telellm version', context_settings=CONTEXT_SETTINGS)
def version():
    """This command calls the `version_cmd` function to display the version."""
    version_cmd()


# 模型测试（功能/性能）
@cli.command('test', short_help='generate functional/performance test reports', context_settings=CONTEXT_SETTINGS)
@click.option('--test_type', '-tt', type=click.Choice(['functional', 'performance', 'both']), default='both',
              help='default:both, type of test report (functional, performance, or both)')
@click.option('--service_host', '-sh', type=str, default='localhost', help='default:localhost, host of the service')
@click.option('--service_port', '-sp', type=int, default=8899, help='default:8899, port of the service')
@click.option('--service_name', '-sn', type=str, default='llmservice', help='llm application name')
@click.option('--model_name', '-mn', type=str, default='model_name', help='llm model name')
@click.option('--concurrency', '-c', type=int, multiple=True, default=[1],
              help='default:[1], concurrency levels for performance testing')
@click.option('--seq_len', '-s', type=int, multiple=True, default=[25, 100, 400, 800],
              help='default:[25, 100, 400, 800], seq length for performance testing')
def test_report(test_type, service_host, service_port, service_name, model_name, concurrency, seq_len):
    """
    Generates functional and/or performance test reports for an LLM service based on specified parameters
    such as test type, service host, port, model name, concurrency levels, and sequence lengths.
    """
    test_report_cmd(test_type, service_host, service_port, service_name, model_name, concurrency, seq_len)


# 模型评测
@cli.command('eval', short_help='evaluating llm on datasets', context_settings=CONTEXT_SETTINGS)
@click.option('--service_host', '-sh', type=str, default='localhost', help='default:localhost, host of the service')
@click.option('--service_port', '-sp', type=int, default=8899, help='default:8899, port of the service')
@click.option('--model_name', '-mn', type=str, default='model_name', help='llm model name')
@click.option('--dataset', '-ds', type=click.Choice(['mmlu', 'ceval', 'humaneval', 'gsm8k']), default='mmlu',
              help='default:mmlu, select the evaluation dataset')
@click.option('--type', '-t', type=click.Choice(['val', 'test']), default='val', help='default:val, dataset\'s type')
@click.option('--overwrite', '-o', is_flag=True, help='default:False, overwrite existed results')
@click.option('--num_threads', '-nt', type=int, default=5, help='default:5, the maximum number of threads executed')
@click.option('--temperature', '-tt', type=float, default=1.0, help='default:1.0, temperature')
@click.option('--top_p', '-tp', type=float, default=0.001, help='default:0.001, top_p')
@click.option('--top_k', '-tk', type=int, default=1, help='default:1, top_k')
@click.option('--repetition_penalty', '-rp', type=float, default=1.0, help='default:1.0, repetition_penalty')
@click.option('--enable_rp', '-erp', is_flag=True, help='default:False, repetition_penalty是否启用(临时)')
def eval_dataset(service_host, service_port, model_name, dataset, type, overwrite, num_threads,
                 temperature, top_p, top_k, repetition_penalty, enable_rp):
    """
    Evaluates an LLM model on selected datasets (mmlu, ceval, humaneval, gsm8k) with configurable parameters such as
    temperature, top_p, top_k, repetition penalty, and concurrency.
    """
    request_param = (temperature, top_p, top_k, repetition_penalty, enable_rp)
    eval_cmd(service_host, service_port, model_name, dataset, type, overwrite, num_threads, request_param)


# 模型量化
@cli.command('quant', short_help='quantify llm', context_settings=CONTEXT_SETTINGS)
@click.option('--model_path', '-mp', type=str, help='model path')
@click.option('--save_directory', '-sd', type=str, help='save directory')
@click.option('--calib_file', '-cf', type=str, default=None, help='calib file')
@click.option('--config_path', '-cp', type=click.Path(readable=True), default='./quant_config.json',
              help='The path of quant config file')
@click.option('--w_bit', '-w', type=int, default=8, help='weight bit')
@click.option('--a_bit', '-a', type=int, default=16, help='activation bit')
@click.option('--w_method', '-wm', type=click.Choice(['MinMax', 'GPTQ', 'HQQ']), default='MinMax',
              help='weight quantization method, `MinMax`: `Min-Max`, `GPTQ`: `GPTQ`, `HQQ`: `HQ-Quant`')
@click.option('--act_method', '-am', type=click.Choice(['1', '2', '3']), default='1',
              help='activation quantization method, `1`: `Min-Max`, `2`: `Histogram`, `3`: `Mix method`')
@click.option('--anti_method', '-aom', type=click.Choice(['m1', 'm2', 'm3']), default=None,
              help='Anti-Outlier method. `m1`:`SmoothQuant`, `m2`:`OutlierSuppression`, `m3`:`AWQ for W8A16`')
@click.option('--disable_names', '-dn', type=object, default=None,
              help='Exclude quantized node names, eg. model.layers.{}.mlp.down_proj')
@click.option('--disable_level', '-dl', type=str, default="L0", help='disable level, `L0`, `L1`, `L2`, and so on')
@click.option('--w_sym', '-ws', type=bool, default=True, help='Whether weightization is symmetrical quantization')
@click.option('--dev_type', '-dt', type=click.Choice(['npu', 'cpu']), default='npu', help='device type')
@click.option('--pr', '-pr', type=click.FloatRange(0, 1), default=1.0, help='Quantifying selection probabilities')
@click.option('--mm_tensor', '-mmt', type=bool, default=False, help='`True`: `per-tensor`, `False`: `per-channel`')
@click.option('--co_sparse', '-cs', type=bool, default=False, help='Whether to sparse quantization')
@click.option('--nonuniform', '-nu', type=bool, default=False, help='Whether to use non-uniform in sparse quantization')
@click.option('--fraction', '-fr', type=float, default=0.011, help='Sparse quantization fraction')
@click.option('--is_lowbit', '-il', type=bool, default=False, help='Whether to lowbit quantize the model')
@click.option('--do_smooth', '-ds', type=bool, default=False, help='Whether to smooth the activation')
@click.option('--use_sigma', '-us', type=bool, default=False, help='Whether to use sigma')
@click.option('--sigma_factor', '-sf', type=click.FloatRange(3, 4), default=3.0, help='The sigma factor')
@click.option('--disable_last_linear', '-dl', type=bool, default=True,
              help="Whether to fall back to the last linear layer")
@click.option('--performance', '-pf', type=bool, default=True, help='Whether to do performance test')
@click.option('--accuracy', '-acc', type=bool, default=False, help='Whether to do accuracy test')
@click.option('--dataset', '-dat', type=click.Choice(['mmlu', 'gsm8k']), default='mmlu',
              help="Choose accuracy dataset from `mmlu` or `gsm8k`")
@click.option('--type', '-tp', type=click.Choice(['val', ' test']), default='val', help='Subsets of the dataset')
@click.option('--num_threads', '-nt', type=int, default=5, help='the maximum number of threads executed')
def quantify_llm(**kwargs):
    """
    Performs model quantization on an LLM, supporting various configuration options like weight and activation bit precision,
    quantization methods, anti-outlier techniques, and optional performance and accuracy tests on datasets like MMLU and GSM8K.
    """
    quantify_cmd(kwargs)


# 量化配置文件
@cli.command('quant_config', short_help='generate quantitative config file', context_settings=CONTEXT_SETTINGS)
def quant_config():
    """
    生成默认量化配置文件
    """
    gen_quant_config()


# 量化测试接口 ！忽略！
@cli.command('perform')
@click.option('--performance', '-pf', type=bool, default=True, help='Whether to do performance test')
@click.option('--accuracy', '-acc', type=bool, default=False, help='Whether to do accuracy test')
@click.option('--dataset', '-dat', type=click.Choice(['mmlu', 'gsm8k']), default='mmlu',
              help="Choose evaluation dataset")
@click.option('--type', '-tp', type=click.Choice(['val', ' test']), default='val', help='Subsets of the dataset')
@click.option('--num_threads', '-nt', type=int, default=5, help='the maximum number of threads executed')
def perform(performance, accuracy, dataset, type, num_threads):
    """
    Performs performance and/or accuracy tests on a specified dataset.
    """
    perform_test(performance, accuracy, dataset, type, num_threads)


# 服务化项目
@cli.command('serve', short_help='start service image', context_settings=CONTEXT_SETTINGS)
@click.option('--model', '-m', type=str, default="/model", help='llm model path')
@click.option('--service_name', '-sn', type=str, default="telellm-infer-svc", help='Service name')
@click.option('--port', '-p', type=str, default=8899, help='Service port number')
@click.option('--model_precision', '-mp', type=str, default='float16', help='llm model precision')
@click.option('--tensor_parallel_size', '-tps', type=str, default=1, help='Number of model tensor parallelism')
@click.option('--topk', '-tk', type=str, default=20, help='Sampling top-k')
@click.option('--temperature', '-t', type=str, default=1.0, help='Sampling temperature')
@click.option('--topp', '-tp', type=str, default=1.0, help='Sampling top-p')
@click.option('--repetition_penalty', '-rp', type=str, default=1.0, help='Sampling repetition penalty')
@click.option('--model_name', '-mn', type=str, default="Qwen2", help='llm model name')
@click.option('--max_num_seq', '-mns', type=str, default=64, help='Maximum number of parallel sequences')
@click.option('--max_length', '-ml', type=str, default=4096, help='Maximum sequence length')
@click.option('--gpu_memory_utilization', '-gmu', type=str, default=0.95, help='GPU memory utilization')
@click.option('--max_num_batched_tokens', '-mnbt', type=str, default=None, help='Maximum number of batched tokens')


def serve(model, service_name, port, model_precision, tensor_parallel_size, topk, temperature, topp,
          repetition_penalty, model_name, max_num_seq, max_length, gpu_memory_utilization, max_num_batched_tokens):
    """
    Starts a service for the specified LLM model with configurable parameters such as precision, tensor parallelism, and sampling settings.
    """
    serve_cmd(model, service_name, port, model_precision, tensor_parallel_size, topk, temperature, topp,
          repetition_penalty, model_name, max_num_seq, max_length, gpu_memory_utilization, max_num_batched_tokens)
    