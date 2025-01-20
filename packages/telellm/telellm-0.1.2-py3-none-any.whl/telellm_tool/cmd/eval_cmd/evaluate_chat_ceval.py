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
"""evaluate_chat_ceval"""
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
from thefuzz import process
from tqdm import tqdm

# wget https://huggingface.co/datasets/ceval/ceval-exam/resolve/main/ceval-exam.zip

TASK_NAME_MAPPING = {
    "computer_network": ["Computer Network", "\u8ba1\u7b97\u673a\u7f51\u7edc", "STEM"],
    "operating_system": ["Operating System", "\u64cd\u4f5c\u7cfb\u7edf", "STEM"],
    "computer_architecture": [
        "Computer Architecture",
        "\u8ba1\u7b97\u673a\u7ec4\u6210",
        "STEM",
    ],
    "college_programming": ["College Programming", "\u5927\u5b66\u7f16\u7a0b", "STEM"],
    "college_physics": ["College Physics", "\u5927\u5b66\u7269\u7406", "STEM"],
    "college_chemistry": ["College Chemistry", "\u5927\u5b66\u5316\u5b66", "STEM"],
    "advanced_mathematics": [
        "Advanced Mathematics",
        "\u9ad8\u7b49\u6570\u5b66",
        "STEM",
    ],
    "probability_and_statistics": [
        "Probability and Statistics",
        "\u6982\u7387\u7edf\u8ba1",
        "STEM",
    ],
    "discrete_mathematics": [
        "Discrete Mathematics",
        "\u79bb\u6563\u6570\u5b66",
        "STEM",
    ],
    "electrical_engineer": [
        "Electrical Engineer",
        "\u6ce8\u518c\u7535\u6c14\u5de5\u7a0b\u5e08",
        "STEM",
    ],
    "metrology_engineer": [
        "Metrology Engineer",
        "\u6ce8\u518c\u8ba1\u91cf\u5e08",
        "STEM",
    ],
    "high_school_mathematics": [
        "High School Mathematics",
        "\u9ad8\u4e2d\u6570\u5b66",
        "STEM",
    ],
    "high_school_physics": ["High School Physics", "\u9ad8\u4e2d\u7269\u7406", "STEM"],
    "high_school_chemistry": [
        "High School Chemistry",
        "\u9ad8\u4e2d\u5316\u5b66",
        "STEM",
    ],
    "high_school_biology": ["High School Biology", "\u9ad8\u4e2d\u751f\u7269", "STEM"],
    "middle_school_mathematics": [
        "Middle School Mathematics",
        "\u521d\u4e2d\u6570\u5b66",
        "STEM",
    ],
    "middle_school_biology": [
        "Middle School Biology",
        "\u521d\u4e2d\u751f\u7269",
        "STEM",
    ],
    "middle_school_physics": [
        "Middle School Physics",
        "\u521d\u4e2d\u7269\u7406",
        "STEM",
    ],
    "middle_school_chemistry": [
        "Middle School Chemistry",
        "\u521d\u4e2d\u5316\u5b66",
        "STEM",
    ],
    "veterinary_medicine": ["Veterinary Medicine", "\u517d\u533b\u5b66", "STEM"],
    "college_economics": [
        "College Economics",
        "\u5927\u5b66\u7ecf\u6d4e\u5b66",
        "Social Science",
    ],
    "business_administration": [
        "Business Administration",
        "\u5de5\u5546\u7ba1\u7406",
        "Social Science",
    ],
    "marxism": [
        "Marxism",
        "\u9a6c\u514b\u601d\u4e3b\u4e49\u57fa\u672c\u539f\u7406",
        "Social Science",
    ],
    "mao_zedong_thought": [
        "Mao Zedong Thought",
        "\u6bdb\u6cfd\u4e1c\u601d\u60f3\u548c\u4e2d\u56fd\u7279\u8272\u793e\u4f1a\u4e3b\u4e49\u7406\u8bba\u4f53\u7cfb\u6982\u8bba",
        "Social Science",
    ],
    "education_science": ["Education Science", "\u6559\u80b2\u5b66", "Social Science"],
    "teacher_qualification": [
        "Teacher Qualification",
        "\u6559\u5e08\u8d44\u683c",
        "Social Science",
    ],
    "high_school_politics": [
        "High School Politics",
        "\u9ad8\u4e2d\u653f\u6cbb",
        "Social Science",
    ],
    "high_school_geography": [
        "High School Geography",
        "\u9ad8\u4e2d\u5730\u7406",
        "Social Science",
    ],
    "middle_school_politics": [
        "Middle School Politics",
        "\u521d\u4e2d\u653f\u6cbb",
        "Social Science",
    ],
    "middle_school_geography": [
        "Middle School Geography",
        "\u521d\u4e2d\u5730\u7406",
        "Social Science",
    ],
    "modern_chinese_history": [
        "Modern Chinese History",
        "\u8fd1\u4ee3\u53f2\u7eb2\u8981",
        "Humanities",
    ],
    "ideological_and_moral_cultivation": [
        "Ideological and Moral Cultivation",
        "\u601d\u60f3\u9053\u5fb7\u4fee\u517b\u4e0e\u6cd5\u5f8b\u57fa\u7840",
        "Humanities",
    ],
    "logic": ["Logic", "\u903b\u8f91\u5b66", "Humanities"],
    "law": ["Law", "\u6cd5\u5b66", "Humanities"],
    "chinese_language_and_literature": [
        "Chinese Language and Literature",
        "\u4e2d\u56fd\u8bed\u8a00\u6587\u5b66",
        "Humanities",
    ],
    "art_studies": ["Art Studies", "\u827a\u672f\u5b66", "Humanities"],
    "professional_tour_guide": [
        "Professional Tour Guide",
        "\u5bfc\u6e38\u8d44\u683c",
        "Humanities",
    ],
    "legal_professional": [
        "Legal Professional",
        "\u6cd5\u5f8b\u804c\u4e1a\u8d44\u683c",
        "Humanities",
    ],
    "high_school_chinese": [
        "High School Chinese",
        "\u9ad8\u4e2d\u8bed\u6587",
        "Humanities",
    ],
    "high_school_history": [
        "High School History",
        "\u9ad8\u4e2d\u5386\u53f2",
        "Humanities",
    ],
    "middle_school_history": [
        "Middle School History",
        "\u521d\u4e2d\u5386\u53f2",
        "Humanities",
    ],
    "civil_servant": ["Civil Servant", "\u516c\u52a1\u5458", "Other"],
    "sports_science": ["Sports Science", "\u4f53\u80b2\u5b66", "Other"],
    "plant_protection": ["Plant Protection", "\u690d\u7269\u4fdd\u62a4", "Other"],
    "basic_medicine": ["Basic Medicine", "\u57fa\u7840\u533b\u5b66", "Other"],
    "clinical_medicine": ["Clinical Medicine", "\u4e34\u5e8a\u533b\u5b66", "Other"],
    "urban_and_rural_planner": [
        "Urban and Rural Planner",
        "\u6ce8\u518c\u57ce\u4e61\u89c4\u5212\u5e08",
        "Other",
    ],
    "accountant": ["Accountant", "\u6ce8\u518c\u4f1a\u8ba1\u5e08", "Other"],
    "fire_engineer": [
        "Fire Engineer",
        "\u6ce8\u518c\u6d88\u9632\u5de5\u7a0b\u5e08",
        "Other",
    ],
    "environmental_impact_assessment_engineer": [
        "Environmental Impact Assessment Engineer",
        "\u73af\u5883\u5f71\u54cd\u8bc4\u4ef7\u5de5\u7a0b\u5e08",
        "Other",
    ],
    "tax_accountant": ["Tax Accountant", "\u7a0e\u52a1\u5e08", "Other"],
    "physician": ["Physician", "\u533b\u5e08\u8d44\u683c", "Other"],
}
hard_list = [
    "advanced_mathematics",
    "discrete_mathematics",
    "probability_and_statistics",
    "college_physics",
    "college_chemistry",
    "high_school_mathematics",
    "high_school_physics",
    "high_school_chemistry",
]
choices = ["A", "B", "C", "D"]


def process_before_extraction(gen, question, choice_dict):
    """
    The function `process_before_extraction` processes a given prompt, question, and choice dictionary
    to generate a model output with the correct answer represented by a letter.
    """
    # Example Prompt:
    # 关于传输层的面向连接服务的特性是____。
    # A. 既不保证可靠，也不保证按序交付
    # B. 不保证可靠，但保证按序交付
    # C. 保证可靠，但不保证按序交付
    # D. 既保证可靠，也保证按序交付
    # Example Model Output：
    # 关于传输层的面向连接服务的特性是既保证可靠，也保证按序交付
    # Processed Output:
    # 答案是D

    question_split = question.rstrip("。").split("。")[-1].split("_")

    # replacing the question
    if len(question_split[0].strip()) > 4:
        gen = gen.replace(question_split[0], "答案是")
    if len(question_split[-1].strip()) > 4:
        gen = gen.replace(question_split[-1], "")

    # replace the choice by letter in the generated sentence
    # from the longest one to the shortest one
    for key, val in sorted(choice_dict.items(), key=lambda x: len(x[1]), reverse=True):
        gen = gen.replace(val.rstrip("。"), key)
    return gen


def count_substr(gen, pattern):
    """
    The function `count_substr` takes a string `gen` and a pattern, and returns the count of occurrences
    of the pattern in the string using regular expressions.
    """
    return len(re.findall(pattern, gen))


def extract_choice(gen, choice_list):
    """
    The function `extract_choice` extracts the correct choice (A, B, C, or D) from a given text based on
    specific patterns and a list of choices.
    """
    # 答案是A | 选项是A | 应该选A选项
    res = re.search(
        r"(?:(?:选|选择|选定)[：:]?\s*|(?:(?:答案|选项)(?![^ABCD]{0,10}?(?:不|非)[^ABCD]{0,10}?(?:是|选|为|：|:|】))[^ABCD]{0,10}?(?: \
        是|选|为|：|:|】))[^ABCD]{0,10}?)(A|B|C|D)(?:选项)?(?:\)|。|\.|，|,|．|、|A|B|C|D|$|：|:|\)|）)",
        gen,
    )

    # A选项正确 | A选项符合题意
    if res is None:
        res = re.search(
            r"(A|B|C|D)(?:选?项)?(?![^ABCD]{0,4}?(?:不|非)[^ABCD]{0,4}?(?:正确|对[的，。：]|符合))[^ABCD]{0,4}?(?:正确|对[的，。：]|符合)",
            gen,
        )

    # 直接输出 A
    if res is None:
        res = re.search(r"^[\(（]?(A|B|C|D)(?:。|\)|）|\.|，|,|．|：|:|$)", gen)

    # 获取第一个出现的字母
    if res is None:
        res = re.search(r"(?<![a-zA-Z])(A|B|C|D)(?![a-zA-Z=])", gen)

    if res is None:
        return choices[choice_list.index(process.extractOne(gen, choice_list)[0])]
    return res.group(1)


def format_example(line):
    """
    The `format_example` function takes a dictionary `line` containing a question and choices, and
    formats them into a string with choices labeled A, B, C, etc.
    """
    example = line["question"] + "\n\n"
    for choice in choices:
        example += f'{choice}. {line[f"{choice}"]}\n'
    return example


def extract_answer(response, row):
    """
    This function extracts the predicted answer based on a response and a question prompt
    provided in a row of data.
    """
    prompt = row["question"]
    gen = process_before_extraction(
        response, prompt, {choice: row[choice] for choice in choices}
    )
    if not isinstance(prompt, str):
        prompt = prompt[0]
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
    The `eval_subject` function evaluates a model's performance on a given subject using a target URL
    and request parameters, with the option to save results to a directory.
    """
    result_path = os.path.join(save_result_dir, f"{subject_name}_result.csv")
    if not overwrite and os.path.exists(result_path):
        print(f"{result_path} existed, skip!")
        score = []
        for (_, datarow), (_, resultrow) in zip(
                test_df.iterrows(), pd.read_csv(result_path).iterrows()
        ):
            pred = extract_answer(resultrow["model_response"], datarow)
            if "answer" in datarow:
                correct = 1 if pred == datarow["answer"] else 0
                score.append(correct)
        if score:
            correct_ratio = 100 * sum(score) / len(score)
        else:
            correct_ratio = 0
        return correct_ratio

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

    if "correctness" in test_df.columns:
        score = test_df["correctness"]
        correct_ratio = 100 * sum(score) / len(score)
    else:
        correct_ratio = 0

    if save_result_dir:
        test_df.to_csv(result_path, encoding="utf-8", index=False)

    return correct_ratio


def cal_ceval(res, model_name):
    """
    The function `cal_ceval` calculates and prints the average accuracy scores for different classes and
    overall, based on the input results and model name.
    """
    acc_sum_dict = {}
    acc_norm_sum_dict = {}
    cnt_dict = {}
    acc_sum = 0.0
    cnt = 0
    hard_cnt = 0
    hard_acc_sum = 0.0
    for tt in res.keys():
        name = tt.split("-")[-1]
        acc_sum += float(res[tt])
        cnt += 1
        class_ = TASK_NAME_MAPPING[name][2]
        if class_ not in acc_sum_dict:
            acc_sum_dict[class_] = 0.0
            acc_norm_sum_dict[class_] = 0.0
            cnt_dict[class_] = 0.0
        if name in hard_list:
            hard_cnt += 1
            hard_acc_sum += float(res[tt])
        acc_sum_dict[class_] += float(res[tt])
        cnt_dict[class_] += 1
    print("\n\n\n")

    table_dict = {"Model": [model_name]}
    for k in ["STEM", "Social Science", "Humanities", "Other"]:
        if k in cnt_dict:
            score = round(acc_sum_dict[k] / cnt_dict[k], 2)
            table_dict[f"{k}"] = [str(score)]
            print(f"{k} acc: {score:.2f}")
    if hard_cnt > 0:
        score = round(hard_acc_sum / hard_cnt, 2)
        table_dict["Average(Hard)"] = [str(score)]
        print(f"Hard acc: {score:.2f}")
    avg = round(acc_sum / cnt, 2)
    table_dict["Average"] = [str(avg)]
    print(f"AVERAGE acc: {avg:.2f}")

    return table_dict


def test_ceval_handler(save_result_dir, output_file):
    """
    This function reads data from CSV files in a directory, extracts specific information, and
    saves the results in a JSON file.
    """
    def extract_data_from_csv(_file_path):
        df = pd.read_csv(_file_path)
        data = df.set_index('id')['model_output'].to_dict()
        return data

    result = {}
    for filename in os.listdir(save_result_dir):
        if filename.endswith('_result.csv'):
            category = filename.replace('_result.csv', '')
            file_path = os.path.join(save_result_dir, filename)
            result[category] = extract_data_from_csv(file_path)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print(f"Data has been written to {output_file}")


def eval_chat_ceval(host, port, model_name, _type, overwrite, num_threads, request_param):
    """
    This function evaluates a chat completion model using a specified host, port, model name,
    type of evaluation data (validation or test), and other parameters, saving the results for further
    analysis or submission for benchmarking.
    """
    target_url = f"http://{host}:{port}/v1/chat/completions"

    print("Note: please use greedy decoding(do_sample=False), and disable repetition penalty(repetition_penalty=1.0)")
    print("chat ceval evaluation starting...")

    eval_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset/ceval"))
    save_result_dir = os.path.join(os.getcwd(), f"eval_chat_outs/{model_name}_ceval_{_type}_eval_result")
    os.makedirs(save_result_dir, exist_ok=True)

    dev_result = {}
    for subject_name in tqdm(TASK_NAME_MAPPING.keys()):
        _df = ""
        if _type == 'val':
            val_file_path = os.path.join(eval_data_path, "val", f"{subject_name}_val.csv")
            val_df = pd.read_csv(val_file_path)
            _df = val_df
        elif _type == 'test':
            test_file_path = os.path.join(eval_data_path, "test", f"{subject_name}_test.csv")
            test_df = pd.read_csv(test_file_path)
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
    if _type == 'val':
        return cal_ceval(dev_result, model_name)
    output_file_path = os.path.join(os.getcwd(), f"{model_name}_ceval_{_type}_eval_result.json")
    test_ceval_handler(save_result_dir, output_file_path)
    print(
        f"请将生成的测试集结果{output_file_path}，在https://cevalbenchmark.com/static/user_interface.html提交来获取测试集评分")
    return None
