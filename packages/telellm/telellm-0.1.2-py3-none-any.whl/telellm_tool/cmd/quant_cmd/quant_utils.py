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
"""quant_utils"""
import os
import json
import shutil
import stat
from easydict import EasyDict as edict
from transformers import AutoConfig


def check_json_config(config_path):
    """
    The function `check_json_config` checks if a JSON configuration file exists, loads its content, and
    ensures that specific keys are not empty.
    """
    if not os.path.exists(config_path):
        return False
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data['model_path'].strip() == '' or data['save_directory'].strip() == '':
            raise ValueError('please specify model_path and save_directory in quant_config.json')
    except json.JSONDecodeError as e:
        raise RuntimeError(f'Error decoding Json: {e}') from e
    return True

def load_config(kwargs, use_json):
    """
    The `load_config` function loads configuration settings from either a dictionary or a JSON
    file, with default values provided for each setting.
    """
    # 设置默认参数
    config = edict({
        "model_path": "",
        "save_directory": "",
        "calib_file": None,
        "w_bit": 8,
        "a_bit": 16,
        "dev_type": "npu",
        "disable_level": "L0",
        "w_sym": True,
        "act_method": 1,
        "w_method": "MinMax",
        "disable_names": None,
        "pr": 1.0,
        "mm_tensor": False,
        "co_sparse": False,
        "nonuniform": False,
        "fraction": 0.011,
        "is_lowbit": False,
        "do_smooth": False,
        "use_sigma": False,
        "sigma_factor": 3.0,
        "disable_last_linear": True,
        "anti_method": None,
        "performance": True,
        "accuracy": False,
        "dataset": "mmlu",
        "type": "val",
        "num_threads": 5
    })
    if use_json:
        with open(kwargs.get('config_path'), encoding='utf-8') as f:
            json_config = json.load(f)
        for key, value in json_config.items():
            if key in config:
                config[key] = value
    else:
        for key, value in kwargs.items():
            if key in config:
                config[key] = int(value) if key == "act_method" else value

    if config.calib_file is not None:
        # 检查 calib_file 是否存在
        if not os.path.exists(config.calib_file):
            raise ValueError(f"{config.calib_file} does not exist")
        # 检查 calib_file 格式问题
        with open(config.calib_file, encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                if 'inputs_pretokenized' not in data:
                    raise ValueError('calib_file is not a valid json file')
    print(config)
    return config


def load_jsonl(dataset_path, key_name='inputs_pretokenized'):
    """加载校准数据集"""
    dataset = []
    with open(dataset_path, encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            text = data[key_name]
            dataset.append(text)
    return dataset

def copy_tokenizer_files(model_dir, dest_dir):
    """
    The function `copy_tokenizer_files` copies files containing specific keywords from a source
    directory to a destination directory.
    """
    os.makedirs(dest_dir, exist_ok=True)
    for filename in os.listdir(model_dir):
        if 'tokenizer' in filename or 'tokenization' in filename or 'generation' in filename or 'special' in filename:
            src_filepath = os.path.join(model_dir, filename)
            dest_filepath = os.path.join(dest_dir, filename)
            shutil.copyfile(src_filepath, dest_filepath)

def modify_config(model_dir, dest_dir, torch_dtype, quantize_type):
    """
    This function modifies a configuration file by updating the torch data type and quantization type
    based on the input parameters.
    """
    src_config_filepath = os.path.join(model_dir, 'config.json')
    with open(src_config_filepath, 'r', encoding='utf-8') as fr:
        data = json.load(fr)
    if 'torch' in str(torch_dtype):
        data['torch_dtype'] = str(torch_dtype).split(".")[1]
    else:
        data['torch_dtype'] = str(torch_dtype)
    data['quantize'] = quantize_type
    dest_config_filtpath = os.path.join(dest_dir, 'config.json')
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    models = stat.S_IWUSR | stat.S_IRUSR
    with os.fdopen(os.open(dest_config_filtpath, flags, models), 'w', encoding='utf-8') as fw:
        json.dump(data, fw, indent=4)

def check_directory(save_directory):
    """检查量化文件保存路径，先清空后创建"""
    if os.path.isdir(save_directory):
        shutil.rmtree(save_directory, ignore_errors=True)

    if not os.path.exists(save_directory):
        os.makedirs(save_directory, exist_ok=True)

def disable_layers(model_path, disable_name):
    """根据传入的disable_name和模型的层数，自动生成需要冻结的层"""
    if disable_name is None:
        return None
    config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
    num_layers = config.num_hidden_layers

    disable_name_prefix = disable_name.split("{")[0]
    disable_name_tail = disable_name.split("}")[1]
    disable_names = [disable_name_prefix + str(layer) + disable_name_tail for layer in range(num_layers)]
    return disable_names

def save_result(origin_model_performance, quant_model_performance, origin_model_accuracy, quant_model_accuracy, config):
    """形成量化报告"""
    with open('quant_result.json', 'w', encoding='utf-8') as f:
        d = {}
        d["quant_config"] = config
        if origin_model_performance != {}:
            d["origin_performance"] = origin_model_performance
            d["quant_performance"] = quant_model_performance
        if origin_model_accuracy != {}:
            d['origin_accuracy'] = origin_model_accuracy
            d['quant_accuracy'] = quant_model_accuracy
        # Convert the dictionary to a JSON string before writing
        json.dump(d, f)
        f.write('\n')  # Add a newline for better readability
    