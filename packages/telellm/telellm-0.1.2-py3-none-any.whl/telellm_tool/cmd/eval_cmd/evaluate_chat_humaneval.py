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
"""evaluate_chat_humaneval"""
import os
import re
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import tqdm

from telellm_tool.cmd.eval_cmd.human_eval.data import stream_jsonl, write_jsonl
from telellm_tool.cmd.eval_cmd.human_eval.evaluation import evaluate_functional_correctness

# https://github.com/openai/human-eval

def extract_code(text, entry_point):
    """正则表达式匹配代码块"""
    code_block_pattern = re.compile(
        rf"```(?:[Pp]ython\n)?.*?def\s+{entry_point}.*?:\n(.*?)\n```", re.DOTALL
    )
    code_block = code_block_pattern.search(text)
    if code_block is None:
        code_block_pattern = re.compile(
            rf"def\s+{entry_point}.*?:\n(.*?)(?:\n(?!\n*(?:  |\t))|$)", re.DOTALL
        )
        code_block = code_block_pattern.search(text)
    if code_block is None:
        code_block_pattern = re.compile(
            r"def.*?:\n(.*?)(?:\n(?!\n*(?:  |\t))|$)", re.DOTALL
        )
        code_block = code_block_pattern.search(text)

    if code_block is not None:
        return code_block.group(1)

    # if no code block is found, assume the LM is simply filling the code
    return textwrap.indent(text, " " * 4)


def generate_sample(jobj, target_url, model_name, index, request_param):
    """use humanevalpack prompt"""
    signature = re.search(
        rf"def\s+({jobj['entry_point']}.*?):\s*\n", jobj["prompt"]
    ).group(1)
    description = "\n".join(
        [
            line.strip()
            for line in re.search(
                r"(?:\"\"\"|''')(.*?)(?:\"\"\"|''')", jobj["prompt"], re.DOTALL
            ).group(1).split("\n")
        ]
    )
    prompt = (
        f"Write a Python function `{signature}` to solve the following problem:\n"
        f"{description}\n"
        f"{jobj['prompt']}"
    )

    task_id = jobj["task_id"]
    question = prompt
    entry_point = jobj["entry_point"]

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
    print(response)
    answer = extract_code(response, entry_point)
    return {"index": index, "task_id": task_id, "completion": answer, "response": response}


def eval_chat_humaneval(host, port, model_name, _type, overwrite, num_threads, request_param):
    """
    The function `eval_chat_humaneval` evaluates a chat model using human evaluation data and outputs
    the results in a JSON file, then verifies the model's performance against the evaluation data.
    """
    target_url = f"http://{host}:{port}/v1/chat/completions"

    print("Note: please use greedy decoding(do_sample=False), and disable repetition penalty(repetition_penalty=1.0)")
    print("chat humaneval evaluation starting...")

    sample_input_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset/humaneval/HumanEval.jsonl.gz"))
    save_result_dir = os.path.join(os.getcwd(), f"eval_chat_outs/{model_name}_humaneval_eval_result")
    os.makedirs(save_result_dir, exist_ok=True)
    sample_output_file = os.path.join(save_result_dir, "HumanEval_res.jsonl")

    if not overwrite and os.path.exists(sample_output_file):
        print(f"{sample_output_file} existed, skip!")
    else:
        def combine_results():
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = {
                    executor.submit(generate_sample, jobj, target_url, model_name, idx, request_param): idx
                    for idx, jobj in enumerate(stream_jsonl(sample_input_file))
                }
                results = [None] * len(futures)
                for future in tqdm.tqdm(as_completed(futures), total=len(futures), desc="task_idx"):
                    result = future.result()
                    results[result["index"]] = result
                return results

        output_results = tqdm.tqdm(combine_results())

        print(f"Writing model response to {sample_output_file}...")
        write_jsonl(sample_output_file, output_results)

    # verify
    pass_at_k = evaluate_functional_correctness(sample_output_file, problem_file=sample_input_file)

    table_dict = {"Model": [model_name]}
    for key in pass_at_k.keys():
        table_dict[key] = [f"{round(pass_at_k.get(key) * 100, 4)}%"]
    print(table_dict)
    return table_dict
