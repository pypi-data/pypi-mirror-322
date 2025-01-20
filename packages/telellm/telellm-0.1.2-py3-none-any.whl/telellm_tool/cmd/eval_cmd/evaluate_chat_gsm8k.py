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
"""evaluate_chat_gsm8k"""
import json
import math
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import requests
import tqdm

# https://github.com/openai/grade-school-math

def generate_sample(doc, target_url, model_name, request_param):
    """
    The function `generate_sample` takes a document, target URL, model name, and request parameters to
    generate a response using a specified model and returns the document with completion and accuracy
    information.
    """
    question = doc['question']

    temperature, top_p, top_k, repetition_penalty, enable_rp = request_param

    req_data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": question}
        ],
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        # "repetition_penalty": repetition_penalty,
        "stream": False,
    }
    if enable_rp:
        req_data["repetition_penalty"] = repetition_penalty
    resp = requests.post(target_url, json=req_data, timeout=60)
    response = ""
    if resp.status_code != 200:
        print(resp.json())
    else:
        response = resp.json()["choices"][0]["message"]["content"]
    print(question)
    print("-------------")
    print(response)
    print("=============")

    completion = response
    answer = doc['answer']
    acc = is_correct(completion, answer)
    doc["completion"] = completion
    doc["acc"] = acc

    return doc, acc


def extract_answer(s):
    """
    The function `extract_answer` extracts the last digit from a given string.
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


def is_correct(completion, answer):
    """
    The function `is_correct` compares two answers for numerical equality with a specified tolerance.
    """
    gold = extract_answer(answer)
    assert gold is not None, "No ground truth answer found in the document."

    def number_equal(answer, pred):
        if pred is None:
            return False
        try:
            return math.isclose(eval(answer), eval(pred), rel_tol=0, abs_tol=1e-4)
        except Exception as e:
            print(f"An error occurred: {e}")
            print(
                f"cannot compare two numbers: answer={answer}, pred={pred}", flush=True
            )
            return False

    return number_equal(gold, extract_answer(completion))


def eval_chat_gsm8k(host, port, model_name, _type, overwrite, num_threads, request_param):
    """
    This function evaluates a chat model using GSM8K dataset and outputs the average accuracy of
    the model.
    """
    target_url = f"http://{host}:{port}/v1/chat/completions"

    print("Note: please use greedy decoding(do_sample=False), and disable repetition penalty(repetition_penalty=1.0)")
    print("chat gsm8k evaluation starting...")

    sample_input_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset/gsm8k/test.jsonl"))
    save_result_dir = os.path.join(os.getcwd(), f"eval_chat_outs/{model_name}_gsm8k_eval_result")
    os.makedirs(save_result_dir, exist_ok=True)
    sample_output_file = os.path.join(save_result_dir, "gsm8k_res.jsonl")

    acc_res = []
    if not overwrite and os.path.exists(sample_output_file):
        test = []
        with open(sample_output_file, 'r', encoding='utf-8') as file:
            for line in file:
                test.append(json.loads(line))

        for doc in tqdm.tqdm(test):
            acc_res.append(doc["acc"])
    else:
        # read sample_input_file
        test = []
        with open(sample_input_file, 'r', encoding='utf-8') as file:
            for line in file:
                test.append(json.loads(line))

        buffer = []
        # write sample_output_file
        with open(sample_output_file, 'w', encoding='utf-8') as f_output:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = {executor.submit(generate_sample, doc, target_url, model_name, request_param): doc for doc in test}
                for future in tqdm.tqdm(as_completed(futures), total=len(test)):
                    doc, acc = future.result()
                    buffer.append(json.dumps(doc, ensure_ascii=False) + "\n")
                    acc_res.append(acc)

                    if len(buffer) >= 100:
                        f_output.writelines(buffer)
                        f_output.flush()
                        buffer.clear()
                if buffer:
                    f_output.writelines(buffer)
                    f_output.flush()

    acc = round(np.mean(acc_res), 4)  # noqa

    print("Acc", acc)
    return {
        "Model": [model_name],
        "Average": [str(acc)]
    }
