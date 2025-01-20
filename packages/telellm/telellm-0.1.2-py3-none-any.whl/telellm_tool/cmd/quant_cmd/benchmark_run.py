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
"""benchmark_run"""
import os
import json
from tqdm import tqdm
import pandas as pd

from telellm_tool.cmd.quant_cmd.inference_engine import InferenceEngine

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


def performance_sync_forward(model_path, queue):
    """
    This function initializes an inference engine with a specified model path, performs a
    warm-up, synchronously runs the inference for performance evaluation, finalizes the engine, and
    returns the result through a queue.
    """
    engine = InferenceEngine(model_path)
    engine.warm_up()
    ret = engine.performance_sync_forward()
    engine.finalize()
    queue.put(ret)


def cal_mmlu(res, task_name_mapping):
    """
    The function `cal_mmlu` calculates and prints the accuracy of different classes and the average
    accuracy based on the input results and task name mapping.
    """
    acc_sum_dict = {}
    acc_norm_sum_dict = {}
    cnt_dict = {}
    acc_sum = 0.0
    cnt = 0

    for class_ in task_name_mapping.keys():
        acc_sum_dict[class_] = 0.0
        acc_norm_sum_dict[class_] = 0.0
        cnt_dict[class_] = 0.0

        for tt in task_name_mapping[class_]:
            acc_sum += sum(res[tt])
            cnt += len(res[tt])

            acc_sum_dict[class_] += sum(res[tt])
            cnt_dict[class_] += len(res[tt])

    print("\n\n\n")

    table_dict = {}
    for k in task_name_mapping.keys():
        if k in cnt_dict:
            score = round(acc_sum_dict[k] * 100 / cnt_dict[k], 2)
            table_dict[f"{k}"] = [str(score)]
            print(f"{k} ACC: {score:.2f}")
    avg = round(acc_sum * 100 / cnt, 2)
    table_dict["Average"] = [str(avg)]
    print(f"AVERAGE ACC: {avg:.2f}")
    return table_dict


def accuracy_sync_forward(dataset, model_path, _type, num_threads, queue):
    """
    The function `accuracy_sync_forward` evaluates the accuracy of a model on a given dataset using
    inference engine and multi-threading, and then puts the results in a queue.
    """
    print("accuracy starting...")
    engine = InferenceEngine(model_path)
    engine.warm_up()

    table_dict = {}
    try:
        if dataset == "mmlu":
            eval_data_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../eval_cmd", "dataset/", dataset))
            result = {}
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
                score = engine.accuracy_sync_forward(dataset, num_threads, _df)
                result[subject_name] = score
            table_dict = cal_mmlu(result, TASK_NAME_MAPPING)
        elif dataset == "gsm8k":
            sample_input_file = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../eval_cmd", "dataset/gsm8k/test.jsonl"))
            test = []
            with open(sample_input_file, 'r', encoding='utf-8') as file:
                for line in file:
                    test.append(json.loads(line))
            table_dict = engine.accuracy_sync_forward(dataset, num_threads, test)
    except Exception as e:
        print(f"An error occurred: {e}")
        engine.finalize()
    engine.finalize()
    queue.put(table_dict)
