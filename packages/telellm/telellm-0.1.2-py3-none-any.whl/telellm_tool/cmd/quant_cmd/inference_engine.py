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
"""inference_engine"""
import json
import os
import time
import threading
import math
from multiprocessing import Queue
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import torch_npu
from tqdm import tqdm
from thefuzz import process
from transformers import AutoTokenizer
from sdk.engine import Engine
from sdk.status import Code
from sdk.request import Request, RequestId
from sdk.data import Data
from sdk.dtype import DType
from sdk.sampling import SamplingParams
from telellm_tool.utils.logging import Logger
from telellm_tool.cmd.test_cmd.test_performance import TextExtractor
from telellm_tool.utils.file_utils import PathCheck


class Tokenizer:
    """The `Tokenizer` class utilizes the Hugging Face Transformers library to tokenize and encode text data."""
    def __init__(self, model_path):
        self.tokenizer_model = AutoTokenizer.from_pretrained(
            model_path, trust_remote_code=True, use_fast=True
        )

    def encode(self, ques_string: str, add_special_tokens=True) -> list:
        """
        The `encode` function takes a question string, encodes it using a tokenizer model, and returns
        the token IDs.
        """
        token_ids = self.tokenizer_model.encode(ques_string, add_special_tokens=add_special_tokens)
        return token_ids

    def decode(self, token_ids: list) -> str:
        """
        The `decode` function takes a list of token IDs and returns the decoded string using a tokenizer
        model.
        """
        output_str = self.tokenizer_model.decode(token_ids)
        return output_str

class InferenceEngine:
    """This class `InferenceEngine` contains methods for initializing an engine, updating model
       configuration, converting input data for inference, performing warm-up, synchronous inference,
       performance testing, and accuracy evaluation for different datasets."""
    def __init__(self, model_path) -> None:
        self.tokenizer = Tokenizer(model_path)
        self.logger = Logger().logger
        self.sampling_params = {}
        self.id_count = 0
        self.do_sampling = False
        self.max_out_len = 2048
        self.model_path = model_path

        self.py_engine = Engine()
        self.init_engine()

        self.max_batch_size = 200

        self.remain_blocks = 0
        self.remain_prefill_slots = 0
        self.remain_prefill_tokens = 0
        self.processing_num = 0
        self.sync_count = 0
        self.choices = ["A", "B", "C", "D"]

    def init_engine(self):
        """
        This function initializes the engine by updating the model configuration and initializing the
        engine, logging errors if necessary.
        """
        self.logger.info("Begin to update model config and init engine")
        if not self.update_model_config():
            self.logger.error("Infer engine update model config failed")
            return
        status = self.py_engine.init()
        if status.get_code().value != Code.OK.value:
            self.logger.error("Infer engine init model failed, please check the service logs.")

    def update_model_config(self) -> bool:
        ''' 读取config.json里的maxBatchSize，覆盖httpsEnabled和modelWeightPath，读取容器内的实际卡数并覆盖'''
        service_path = os.getenv("MIES_INSTALL_PATH")
        # ServicePath有可能为软链接路径，需要转换
        service_path = os.path.realpath(service_path)
        ret, infos = PathCheck.check_path_full(service_path)
        if not ret:
            self.logger.error(infos)
            return False

        model_config_path = os.path.join(service_path, "conf/config.json")
        if os.path.islink(model_config_path):
            self.logger.error("This config.json is a soft-link, please check")
            return False
        if os.path.exists(model_config_path):
            count = torch_npu.npu.device_count()
            try:
                fd = os.open(model_config_path, os.O_RDWR)
                with os.fdopen(fd, "r+") as file:
                    model_deploy_param = "ModelDeployParam"
                    model_param = "ModelParam"
                    model_config = json.load(file)
                    model_config["OtherParam"]["ServeParam"]["httpsEnabled"] = False
                    # model_config[model_deploy_param][model_param][0]["modelName"] = self.model_name
                    model_config[model_deploy_param][model_param][0]["modelWeightPath"] = self.model_path
                    model_config[model_deploy_param]["npuDeviceIds"] = [list(range(count))]
                    model_config[model_deploy_param][model_param][0]["worldSize"] = count
                    self.max_batch_size = model_config["ScheduleParam"]["maxBatchSize"]
                    file.seek(0)
                    file.truncate()
                    json.dump(model_config, file, indent=4)
                return True
            except Exception as e:
                self.logger.error(f"Infer engine update config failed : {e}")
                return False
        else:
            self.logger.error(f"Infer engine config not found: {model_config_path}")
            return False
    def convert_to_request(self, id_key: str, token_ids: list):
        """
        The function `convert_to_request` takes an `id_key` and a list of `token_ids`, converts them
        into a request object with specified parameters, and returns the request.
        """
        data_size = len(token_ids)
        shape = np.array([1, data_size], dtype=np.int64)
        engine_data = Data()
        engine_data.set_token_id(DType.TYPE_INT64, shape, np.array(token_ids, dtype=np.int64))

        request = Request(RequestId(id_key))
        request.set_data_to_request(engine_data)
        if self.do_sampling:
            request.set_sampling_params(SamplingParams(
                self.sampling_params.get('temperature', 1.0),
                self.sampling_params.get('top_k', 1),
                self.sampling_params.get('top_p', 1.0),
                self.sampling_params.get('typical_p', 1.0),
                self.do_sampling,
                self.sampling_params.get('seed', 1),
                self.sampling_params.get('repetition_penalty', 1.0),
                self.sampling_params.get('watermark', False)
            ))
        request.set_max_output_len(self.max_out_len)
        return request

    def warm_up(self, warm_up_size = 4):
        """
        The `warm_up` function initializes multiple threads to handle requests for warming up a model by
        encoding a given question and executing a specified number of warm-up iterations.
        """
        self.logger.info("Warm up start...")
        question = ("Claire makes a 3 egg omelet every morning for breakfast.  "
                "How many dozens of eggs will she eat in 4 weeks?")
        token_ids = self.tokenizer.encode(question)
        warm_start = time.time()
        warm_up_threads = []
        for i in range(warm_up_size):
            id_key = "warm_up" + str(i)
            request = self.convert_to_request(id_key, token_ids)
            t = threading.Thread(target=self._warm_up_func, args=(request,))
            warm_up_threads.append(t)
            t.start()
        for t in warm_up_threads:
            t.join()
        time_elasped = time.time() - warm_start
        self.logger.info("Warm up finished. Handling %d requests, cost warm up time %.3f seconds",
                        warm_up_size, time_elasped)

    def _warm_up_func(self, request):
        self.py_engine.sync_forward(request)

    def finalize(self):
        """
        The `finalize` function calls the `finalize` method of the `py_engine` attribute of the object
        it belongs to.
        """
        self.py_engine.finalize()

    def sync_thread_infer(self, input_data, q):
        """同步性能测试推理，获取输入tokens, 输出tokens, 生成时间, 首token响应时间, 非首token平均token生成时间, 吞吐量(不包含首token), 吞吐量(包含首token)"""
        token_ids = self.tokenizer.encode(input_data["data"])
        request = self.convert_to_request(input_data["id"], token_ids)
        time_start = time.perf_counter()

        error_record = ""
        prompt_tokens, completion_tokens, first_token_time, generate_time, per_token_time, fps, ffps = 0, 0, 0, 0, 0, 0, 0
        prompt_tokens = len(token_ids)
        status, request_info = self.py_engine.sync_forward(request)
        if status.is_ok():
            # 生成时间
            generate_time = time.perf_counter() - time_start
            # print(f"generate_time: ",generate_time)
            completion_tokens = len(request_info.tokenIds)
            # print(f"gen_tokens: ",completion_tokens)
            start_time = request_info.startTime
            # print(f"start_time: ",start_time)
            response_times = request_info.responseTimes
            first_token_time = (response_times[0] - start_time) / 1000
            # print(f"first_token_time: ",first_token_time)

            # 非首token平均token生成时间(s)
            new_tokens = completion_tokens  # - input_tokens
            per_token_time = (generate_time - first_token_time) / (new_tokens - 1) if (new_tokens - 1) > 0 else 0
            # 吞吐量(不包含首token)(tokens/s)
            fps = 1.0 / per_token_time if per_token_time != 0 else 0
            # 吞吐量(包含首token)(tokens/s)
            ffps = new_tokens / generate_time

        self.logger.info("generate time: %.3f, generate tokens: %d, first token time: %.4f ",generate_time, completion_tokens, first_token_time)
        # 输入tokens, 输出tokens, 生成时间, 首token响应时间, 非首token平均token生成时间, 吞吐量(不包含首token), 吞吐量(包含首token)
        print([prompt_tokens, completion_tokens, generate_time, first_token_time, per_token_time, fps, ffps, error_record])
        q.put([prompt_tokens, completion_tokens, generate_time, first_token_time, per_token_time, fps, ffps, error_record])

    def performance_sync_forward(self, seq_len=None, concurrency=None):
        """
        The `performance_sync_forward` function evaluates the performance of a text extraction model
        with varying concurrency levels and sequence lengths, collecting metrics such as input/output
        tokens, generation time, throughput, and error records.
        """
        if seq_len is None:
            seq_len=[25, 100, 400, 800]
        if concurrency is None:
            concurrency=[1]

        text_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_cmd", "ToLIVE_YuHua.txt"))
        extractor = TextExtractor(text_path)

        for num in concurrency:
            for seq in seq_len:
                print(f"performance test, concurrency: {num}, seq-length: {seq}, evaluating...")
                processes = []
                q = Queue()

                # start_time = time.perf_counter()

                for _ in range(num):
                    query = extractor.extract(seq - 16) + "\n请基于以上内容 续写500字文章"
                    input_data = {
                        "id": str(self.id_count),
                        "data": query,
                        "options": [],
                    }
                    self.id_count += 1
                    processes.append(
                        threading.Thread(target=self.sync_thread_infer, args=(input_data, q))
                    )
                for pro in processes:
                    pro.start()
                for pro in processes:
                    pro.join()

                all_input_tokens, all_output_tokens, all_tokens = 0, 0, 0
                all_generate_time, all_first_token_time, all_per_token_time = 0, 0, 0
                all_fps, all_ffps = 0, 0
                all_error_record = ""
                q_id = 0
                while not q.empty():
                    q_id += 1

                    (
                        input_tokens, output_tokens,
                        generate_time, first_token_time, per_token_time,
                        fps, ffps,
                        error_record
                    ) = q.get()

                    all_input_tokens += input_tokens
                    all_output_tokens += output_tokens
                    all_tokens += (input_tokens + output_tokens)
                    all_generate_time += generate_time
                    all_first_token_time += first_token_time
                    all_per_token_time += per_token_time
                    all_fps += fps
                    all_ffps += ffps
                    if error_record:
                        all_error_record += f"[{q_id} of {num}: {error_record}]\t"

                # 模型 | 并发数 | seq-length
                # | 输入tokens | 输出tokens | 总体tokens
                # | 生成时间 | 首token响应时间 | 非首token平均token生成时间
                # | 每请求吞吐量(不包含首token) | 平均吞吐量 | 平均吞吐率
                # avg_input_tokens = int(all_input_tokens / num)
                # avg_output_tokens = int(all_output_tokens / num)
                # avg_tokens = int(all_tokens / num)
                # avg_generate_time = round(all_generate_time / num, 5) if avg_output_tokens else "/"
                avg_first_token_time = round(all_first_token_time / num, 5)
                # avg_per_token_time = round(all_per_token_time / num, 5) if avg_output_tokens else "/"
                avg_fps = round(all_fps / num, 5)
                avg_ffps = round(all_ffps / num, 5)

                # 端到端的时间
                # end_to_end_time = time.perf_counter() - start_time
                # avg_end_to_end_time = end_to_end_time / num
                # 平均吞吐率
                # batch_size = 1
                # world_size = 1  # 并行推理进程数
                # avg_throughput = round(batch_size * world_size / avg_end_to_end_time, 5) if avg_input_tokens else "/"

                print("performance test, eval step finished, time sleep 1s")
                time.sleep(1)
        res_dict = {}
        res_dict["avg_first_token_time"] = avg_first_token_time
        res_dict["avg_fps"] = avg_fps
        res_dict["avg_ffps"] = avg_ffps
        return res_dict

    def accuracy_sync_forward(self, dataset, num_threads, test_content):
        """
        The `accuracy_sync_forward` function evaluates model performance on different datasets using
        multithreading and returns the accuracy scores.
        """
        self.logger.info("accuracy starting...")
        if dataset == "mmlu":
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = {executor.submit(self.eval_mmlu_format_prompt, row): index
                        for index, row in test_content.iterrows()}
                for future in tqdm(as_completed(futures), total=len(test_content)):
                    try:
                        row_index = futures[future]
                        status, row, _, response = future.result()
                        if status.is_ok():
                            # print(f"response: ", response)
                            pred = self.extract_mmlu_answer(response, row)
                            test_content.at[row_index, "model_response"] = response
                            test_content.at[row_index, "model_output"] = pred
                            if "answer" in row:
                                correct = 1 if pred == row["answer"] else 0
                                test_content.at[row_index, "correctness"] = correct
                    except Exception as e:
                        print(f"Error retrieving result: {e}")
            score = test_content["correctness"] if "correctness" in test_content.columns else []
            return score
        if dataset == "gsm8k":
            acc_res = []
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = {executor.submit(self.eval_gsm8k_format_prompt, doc): doc for doc in test_content}
                for future in tqdm(as_completed(futures), total=len(test_content)):
                    status, row, _, response = future.result()
                    # print("status: ", status.is_ok())
                    if status.is_ok():
                        # print(f"response: ", response)
                        acc = self.extract_gsm8k_answer(response, row['answer'])
                        acc_res.append(acc)
            acc = round(np.mean(acc_res), 4)
            print("Acc", acc)
            return {
                "Average": [str(acc)]
            }

    def eval_mmlu_format_prompt(self, row):
        """
        This function takes a row of data containing a multiple-choice question and its choices, formats
        the question prompt, encodes it using a tokenizer, sends a request to a Python engine for
        evaluation, decodes the response, and returns the status, question, and response.
        """
        question = (
                "The following is a multiple-choice question. Please choose the most suitable one among A, B, C and D as the answer to this question.\n\n"
                + row["question"]
                + "\n"
        )
        for choice in self.choices:
            question += f'{choice}. {row[f"{choice}"]}\n'
        token_ids = self.tokenizer.encode(question)
        request = self.convert_to_request(str(self.id_count), token_ids)
        self.id_count += 1
        status, request_info = self.py_engine.sync_forward(request)
        response = self.tokenizer.decode(request_info.tokenIds)
        return status, row, question, response

    def eval_gsm8k_format_prompt(self, row):
        """
        The function `eval_gsm8k_format_prompt` encodes a question, sends a request to a PyEngine,
        decodes the response, and returns the status, question, and response.
        """
        question = row['question']
        token_ids = self.tokenizer.encode(question)
        request = self.convert_to_request(str(self.id_count), token_ids)
        self.id_count += 1
        status, request_info = self.py_engine.sync_forward(request)
        response = self.tokenizer.decode(request_info.tokenIds)
        return status, row, question, response


    def process_before_extraction(self, gen, choice_dict):
        """
        The function `process_before_extraction` replaces choices in a generated sentence with
        corresponding letters based on a dictionary, prioritizing longer choices.
        """
        # replace the choice by letter in the generated sentence
        # from the longest one to the shortest one
        for key, val in sorted(choice_dict.items(), key=lambda x: len(str(x[1])), reverse=True):
            val = str(val)
            pattern = re.compile(re.escape(val.rstrip(".")), re.IGNORECASE)
            gen = pattern.sub(key, gen)
        return gen

    def extract_mmlu_choice(self, gen, choice_list):
        """
        This function extracts the correct choice (A, B, C, or D) from a given text based on
        various patterns and conditions.
        """
        # answer is A | choice is A | choose A
        res = re.search(
            r"(?:(?:[Cc]hoose)|(?:(?:[Aa]nswer|[Cc]hoice)(?![^ABCD]{0,20}?(?:n't|not))[^ABCD]{0,10}?\b(?:|is|:|be))\b)[^ABCD]{0,20}?\b(A|B|C|D)\b",
            gen,
        )

        # A is correct | A is right
        if res is None:
            res = re.search(
                r"\b(A|B|C|D)\b(?![^ABCD]{0,8}?(?:n't|not)[^ABCD]{0,5}?(?:correct|right))[^ABCD]{0,10}?\b(?:correct|right)\b",
                gen,
            )

        # straight answer: A
        if res is None:
            res = re.search(r"^(A|B|C|D)(?:\.|,|:|$)", gen)

        # simply extract the first appearred letter
        if res is None:
            res = re.search(r"(?<![a-zA-Z])(A|B|C|D)(?![a-zA-Z=])", gen)

        if res is None:
            return self.choices[choice_list.index(process.extractOne(gen, choice_list)[0])]
        return res.group(1)

    def extract_mmlu_answer(self, response, row):
        """
        The function `extract_mmlu_answer` takes a response and a row, processes the data, extracts the
        most likely choice, and returns the prediction.
        """
        gen = self.process_before_extraction(
            response, {choice: row[choice] for choice in self.choices}
        )
        pred = self.extract_mmlu_choice(gen, [row[choice] for choice in self.choices])
        return pred

    def extract_answer(self, s):
        """
        The function `extract_answer` extracts the last digit from a given string `s`.
        """
        PAT_LAST_DIGIT = re.compile(
            r"([+-])?(?=([0-9]|\.[0-9]))(0|([1-9](\d{0,2}(,\d{3})*)|\d*))?(\.\d*)?(?=\D|$)"
        )
        match = list(PAT_LAST_DIGIT.finditer(s))
        if match:
            last_digit = match[-1].group().replace(",", "").replace("+", "").strip()
            # print(f"The last digit in {s} is {last_digit}")
        else:
            last_digit = None
            print(f"No digits found in {s!r}", flush=True)
        return last_digit

    def extract_gsm8k_answer(self, completion, answer):
        """
        The function `extract_gsm8k_answer` compares two numbers extracted from completion and answer
        texts with a tolerance of 1e-4.
        """
        gold = self.extract_answer(answer)
        assert gold is not None, "No ground truth answer found in the document."

        def number_equal(answer, pred):
            if pred is None:
                return False
            try:
                return math.isclose(eval(answer), eval(pred), rel_tol=0, abs_tol=1e-4)
            except Exception as e:
                print(
                    f"cannot compare two numbers: answer={answer}, pred={pred}", flush=True
                )
                print(f"An error occurred: {e}")
                return False

        return number_equal(gold, self.extract_answer(completion))
    