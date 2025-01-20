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
"""test_performance"""
# -*- coding:utf-8 -*-
import json
import os
import re
import time
from multiprocessing import Process
from multiprocessing import Queue

import requests

from telellm_tool.utils.markdown_utils import MarkdownTable


# fastapi 服务并发测试工具
class TextExtractor:
    """
    A class to extract chunks of text from a file, removing whitespace and tracking the current position.
    """
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.text = re.sub(r'\s+', '', file.read())
        self.current_position = 0

    def extract(self, length):
        """
        Extracts a portion of text starting from the current position, and updates the position for the next extraction.
        Returns an empty string if the current position exceeds the text length.
        """
        if self.current_position >= len(self.text):
            return ""  # 如果当前位置已经超过文本长度，返回空字符串

        end_position = self.current_position + length
        extracted_text = self.text[self.current_position:end_position]
        self.current_position = end_position  # 更新当前位置
        return extracted_text


def infer(target_url, req_data, q):
    """
    Sends a POST request to the target URL with the provided data, processes the response to calculate 
    various metrics (e.g., token usage, generation time, throughput), and returns the results.
    """
    time_start = time.perf_counter()

    error_record = ""
    prompt_tokens, completion_tokens, first_token_time, generate_time, per_token_time, fps, ffps = 0, 0, 0, 0, 0, 0, 0
    try:
        resp = requests.post(target_url, json=req_data, stream=True, timeout=60)

        if resp.status_code != 200:
            print("Send fail.")
            try:
                info = resp.json()
            except Exception:
                info = resp

            print(info)
            error_record = info
        else:
            chunk = None
            first_token_flag = True
            second_token_flag = False
            is_contain_usage = False
            is_contain_token = False
            for line in resp.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data:'):
                        content = decoded_line[5:]
                        if content.strip() == '[DONE]':
                            break
                        chunk = json.loads(content)
                        if 'choices' in chunk:
                            for choice in chunk['choices']:
                                if 'delta' in choice:
                                    # 首Token时间计算
                                    if first_token_flag:
                                        if 'role' in choice['delta']:
                                            first_token_time = time.perf_counter() - time_start
                                        first_token_flag = False
                                        second_token_flag = True
                                        continue
                                    if second_token_flag:
                                        if 'role' not in choice['delta'] and 'content' in choice['delta']:
                                            first_token_time = time.perf_counter() - time_start
                                        second_token_flag = False
                        if 'usage' in chunk and chunk['usage']:
                            is_contain_usage = True
                        if 'input_tokens' in chunk and 'output_tokens' in chunk:
                            is_contain_token = True

            if chunk is None:
                raise Exception("服务接口没有返回，请检查服务是否正常.")
            if is_contain_usage:
                # 0.2.0 ↑
                prompt_tokens = chunk['usage']['prompt_tokens']
                completion_tokens = chunk['usage']['completion_tokens']
            elif is_contain_token:
                # 0.1.6 ↓
                prompt_tokens = chunk['input_tokens']
                completion_tokens = chunk['output_tokens']
            else:
                raise Exception("返回不包含token计数信息，请确保服务接口是否正确")

            # 生成时间
            generate_time = time.perf_counter() - time_start
            # 非首token平均token生成时间(s)
            new_tokens = completion_tokens  # - input_tokens
            per_token_time = (generate_time - first_token_time) / (new_tokens - 1) if (new_tokens - 1) > 0 else 0
            # 吞吐量(不包含首token)(tokens/s)
            fps = 1.0 / per_token_time if per_token_time != 0 else 0
            # 吞吐量(包含首token)(tokens/s)
            ffps = new_tokens / generate_time
    except Exception as e:
        print(f"post timeout.{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}. {str(e)}")
        error_record = str(e)

    # 输入tokens, 输出tokens, 生成时间, 首token响应时间, 非首token平均token生成时间, 吞吐量(不包含首token), 吞吐量(包含首token)
    q.put([prompt_tokens, completion_tokens, generate_time, first_token_time, per_token_time, fps, ffps, error_record])


def run_multi_task(config):
    """
    Runs a multi-task performance test by simulating concurrent inference requests with different sequence lengths, 
    collects key metrics such as token counts, response times, throughput, and generates a detailed Markdown report.
    """
    target_url = config.get("target_url")
    nums = config.get("nums")
    model_name = config.get("model_name")
    seq_len = config.get("seq_len")
    warmup_input = "Common sense questions and answers\n\nQuestion: What is the capital of France\nFactual answer:"

    text_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ToLIVE_YuHua.txt"))
    extractor = TextExtractor(text_path)

    # warm up
    print("performance test, warm up start.")
    req_data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": warmup_input}
        ],
        "max_tokens": 512,
        "stream": True,
        "stream_options": {"include_usage": True}
    }
    q = Queue()
    infer(target_url, req_data, q)
    time.sleep(3)  # 减少抖动带来的影响
    while not q.empty():
        q.get()
    q.close()
    print("performance test, warm up finish. time sleep 3s...")
    time.sleep(3)

    # md 表格
    md_table = MarkdownTable()
    md_table.add_header(["模型", "并发数", "seq-length", "平均输入tokens", "平均输出tokens", "平均总体tokens"])
    md_table.add_header(["每请求平均生成时间（s）", "首token平均响应时间（s）", "非首token平均token生成时间(s)"])
    md_table.add_header(
        ["每请求吞吐量(不包含首token)(tokens/s)", "每请求吞吐量(包含首token)（tokens/s）", "平均吞吐率(samples/s)"])

    md_error_record = ""

    # eval
    for num in nums:
        # 25 length > 32 token
        # 100 length > 128 token
        # 400 length > 512 token
        # 800 length > 1024 token
        for seq in seq_len:
            print(f"performance test, concurrency: {num}, seq-length: {seq}, evaluating...")
            processes = []
            q = Queue()

            start_time = time.perf_counter()

            for _ in range(num):
                query = extractor.extract(seq - 16) + "\n请基于以上内容 续写500字文章"
                req_data = {
                    "model": model_name,
                    "messages": [
                        {"role": "user", "content": query}
                    ],
                    "stream": True,
                    "stream_options": {"include_usage": True}
                }

                processes.append(
                    Process(target=infer, args=(target_url, req_data, q))
                )
            for process in processes:
                process.start()
            for process in processes:
                process.join()

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
            avg_input_tokens = int(all_input_tokens / num)
            avg_output_tokens = int(all_output_tokens / num)
            avg_tokens = int(all_tokens / num)
            avg_generate_time = round(all_generate_time / num, 5) if avg_output_tokens else "/"
            avg_first_token_time = round(all_first_token_time / num, 5)
            avg_per_token_time = round(all_per_token_time / num, 5) if avg_output_tokens else "/"
            avg_fps = round(all_fps / num, 5)
            avg_ffps = round(all_ffps / num, 5)

            # 端到端的时间
            end_to_end_time = time.perf_counter() - start_time
            avg_end_to_end_time = end_to_end_time / num
            # 平均吞吐率
            batch_size = 1
            world_size = 1  # 并行推理进程数
            avg_throughput = round(batch_size * world_size / avg_end_to_end_time, 5) if avg_input_tokens else "/"

            md_table.add_row([
                model_name, num, seq, avg_input_tokens, avg_output_tokens, avg_tokens,
                avg_generate_time, avg_first_token_time, avg_per_token_time,
                avg_fps, avg_ffps, avg_throughput
            ])

            # 模型 并发数 seq-length 错误记录
            if all_error_record:
                md_error_record += f"**{model_name} | {num} | {seq} |** {all_error_record} <br />"

            for process in processes:
                if process.is_alive:
                    process.terminate()

            print("performance test, eval step finished, time sleep 1s")
            time.sleep(1)

    table_markdown_str = md_table.to_markdown()
    if md_error_record != "":
        table_markdown_str += f"\n\n注: 测试结果出现异常, 以下为可能原因:\n" \
                              f"> {md_error_record}"
    return table_markdown_str


def get_inference_info(host="localhost", port=8899, model_name="", concurrency=None, seq_len=None):
    """
    Collects inference performance data by running a multi-task test with specified concurrency and sequence lengths,
    and returns a Markdown report summarizing the results.
    """
    if concurrency is None:
        concurrency = [1]
    if seq_len is None:
        seq_len=[25, 100, 400, 800]
    target_url = f"http://{host}:{port}/v1/chat/completions"

    _config = {
        "target_url": target_url,
        "nums": concurrency,  # 并发数
        "model_name": model_name,
        "seq_len": seq_len,
    }

    ret = ""
    try:
        ret = run_multi_task(_config)
    except Exception as e:
        print(f"get_inference_info error, {e}")

    return ret
