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
"""evaluate_chat_mmlu"""
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
from thefuzz import process
from tqdm import tqdm

# wget https://people.eecs.berkeley.edu/~hendrycks/data.tar

TASK_NAME_MAPPING = {
    "STEM": [
        "abstract_algebra",
        "anatomy",
        "astronomy",
        "college_biology",
        "college_chemistry",
        "college_computer_science",
        "college_mathematics",
        "college_physics",
        "computer_security",
        "conceptual_physics",
        "electrical_engineering",
        "elementary_mathematics",
        "high_school_biology",
        "high_school_chemistry",
        "high_school_computer_science",
        "high_school_mathematics",
        "high_school_physics",
        "high_school_statistics",
        "machine_learning",
    ],
    "Social Science": [
        "econometrics",
        "high_school_geography",
        "high_school_government_and_politics",
        "high_school_macroeconomics",
        "high_school_microeconomics",
        "high_school_psychology",
        "human_sexuality",
        "professional_psychology",
        "public_relations",
        "security_studies",
        "sociology",
        "us_foreign_policy",
    ],
    "Humanities": [
        "formal_logic",
        "high_school_european_history",
        "high_school_us_history",
        "high_school_world_history",
        "international_law",
        "jurisprudence",
        "logical_fallacies",
        "moral_disputes",
        "moral_scenarios",
        "philosophy",
        "prehistory",
        "professional_law",
        "world_religions",
    ],
    "Other": [
        "business_ethics",
        "college_medicine",
        "human_aging",
        "management",
        "marketing",
        "medical_genetics",
        "miscellaneous",
        "nutrition",
        "professional_accounting",
        "professional_medicine",
        "virology",
        "global_facts",
        "clinical_knowledge",
    ],
}
SUBJECTS = [v for vl in TASK_NAME_MAPPING.values() for v in vl]
choices = ["A", "B", "C", "D"]


def format_example(line):
    """
    The function `format_example` takes a dictionary representing a multiple-choice question and its
    choices, and formats it into a readable text format.
    """
    example = (
            "The following is a multiple-choice question. Please choose the most suitable one among A, B, C and D as the answer to this question.\n\n"
            + line["question"]
            + "\n"
    )
    for choice in choices:
        example += f'{choice}. {line[f"{choice}"]}\n'
    return example


def process_before_extraction(gen, choice_dict):
    """replace the choice by letter in the generated sentence from the longest one to the shortest one"""
    for key, val in sorted(choice_dict.items(), key=lambda x: len(str(x[1])), reverse=True):
        val = str(val)
        pattern = re.compile(re.escape(val.rstrip(".")), re.IGNORECASE)
        gen = pattern.sub(key, gen)
    return gen


def extract_choice(gen, choice_list):
    """
    The function `extract_choice` extracts the correct answer choice (A, B, C, or D) from a given text
    based on various patterns and rules.
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
        return choices[choice_list.index(process.extractOne(gen, choice_list)[0])]
    return res.group(1)


def extract_answer(response, row):
    """
    The function `extract_answer` takes a response and a row, processes the data before extraction, and
    then extracts a choice based on the processed data.
    """
    gen = process_before_extraction(
        response, {choice: row[choice] for choice in choices}
    )
    pred = extract_choice(gen, [row[choice] for choice in choices])
    return pred


def send_request(row, model_name, target_url, request_param):
    """
    The function `send_request` sends a POST request to a target URL with specified parameters and
    returns the row, question, and response.
    """
    question = format_example(row)

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
    return row, question, resp


def eval_subject(
        target_url,
        model_name,
        request_param,
        num_threads,
        subject_name,
        test_df,
        save_result_dir=None,
        overwrite=False,
):
    """
    The `eval_subject` function evaluates a model on a given test dataset, sending requests to a target
    URL and saving the results to a CSV file.
    """
    result_path = os.path.join(save_result_dir, f"{subject_name}_result.csv")
    if not overwrite and os.path.exists(result_path):
        print(f"{result_path} existed, skip!")
        score = []
        for (_, datarow), (_, resultrow) in zip(
                test_df.iterrows(), pd.read_csv(result_path).astype(str).iterrows()
        ):
            pred = resultrow["model_output"]
            correct = 1 if pred == datarow["answer"] else 0
            score.append(correct)
        return score

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(send_request, row, model_name, target_url, request_param): index
                   for index, row in test_df.iterrows()}
        for future in tqdm(as_completed(futures), total=len(test_df)):
            row_index = futures[future]
            row, question, resp = future.result()
            if resp.status_code != 200:
                print(resp.json())
                continue

            response = resp.json()["choices"][0]["message"]["content"]

            print(question)
            print(response)
            pred = extract_answer(response, row)
            print(pred)
            print("======================")

            test_df.at[row_index, "model_response"] = response
            test_df.at[row_index, "model_output"] = pred
            if "answer" in row:
                correct = 1 if pred == row["answer"] else 0
                test_df.at[row_index, "correctness"] = correct

    score = test_df["correctness"] if "correctness" in test_df.columns else []

    if save_result_dir:
        test_df.to_csv(result_path, encoding="utf-8", index=False)

    return score


def cal_mmlu(res, model_name):
    """
    The function `cal_mmlu` calculates and prints the accuracy of a model for different tasks and
    returns a dictionary with the results.
    """
    acc_sum_dict = {}
    acc_norm_sum_dict = {}
    cnt_dict = {}
    acc_sum = 0.0
    cnt = 0

    for class_, tasks in TASK_NAME_MAPPING.items():
        acc_sum_dict[class_] = 0.0
        acc_norm_sum_dict[class_] = 0.0
        cnt_dict[class_] = 0.0

        for tt in tasks:
            acc_sum += sum(res[tt])
            cnt += len(res[tt])

            acc_sum_dict[class_] += sum(res[tt])
            cnt_dict[class_] += len(res[tt])


    print("\n\n\n")

    table_dict = {"Model": [model_name]}
    for k in TASK_NAME_MAPPING:
        if k in cnt_dict:
            score = round(acc_sum_dict[k] * 100 / cnt_dict[k], 2)
            table_dict[f"{k}"] = [str(score)]
            print(f"{k} ACC: {score:.2f}")
    avg = round(acc_sum * 100 / cnt, 2)
    table_dict["Average"] = [str(avg)]
    print(f"AVERAGE ACC: {avg:.2f}")
    return table_dict


def eval_chat_mmlu(host, port, model_name, _type, overwrite, num_threads, request_param):
    """
    The function `eval_chat_mmlu` evaluates a chat model using MMLU datasets.
    """
    target_url = f"http://{host}:{port}/v1/chat/completions"

    print("Note: please use greedy decoding(do_sample=False), and disable repetition penalty(repetition_penalty=1.0)")
    print("chat mmlu evaluation starting...")

    eval_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset/mmlu"))
    save_result_dir = os.path.join(os.getcwd(), f"eval_chat_outs/{model_name}_mmlu_{_type}_eval_result")
    os.makedirs(save_result_dir, exist_ok=True)

    dev_result = {}
    for subject_name in tqdm(SUBJECTS):
        _df = ""
        if _type == 'val':
            val_file_path = os.path.join(eval_data_path, 'val', f'{subject_name}_val.csv')
            val_df = pd.read_csv(val_file_path, names=['question', 'A', 'B', 'C', 'D', 'answer'])
            _df = val_df
        elif _type == 'test':
            test_file_path = os.path.join(eval_data_path, "test", f"{subject_name}_test.csv")
            test_df = pd.read_csv(
                test_file_path, names=["question", "A", "B", "C", "D", "answer"]
            ).astype(str)
            _df = test_df

        score = eval_subject(
            target_url,
            model_name,
            request_param,
            num_threads,
            subject_name,
            _df,
            save_result_dir,
            overwrite=overwrite,
        )
        dev_result[subject_name] = score
    return cal_mmlu(dev_result, model_name)
