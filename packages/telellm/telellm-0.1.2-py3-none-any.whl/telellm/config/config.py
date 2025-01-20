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

# -*- coding:utf-8 -*-
"""
配置文件, 分动态配置和静态配置
"""
import logging
import os

import torch
from easydict import EasyDict as edict

logger = logging.getLogger(__name__)

# 配置固定环境变量
if not os.environ.get("PYTORCH_CUDA_ALLOC_CONF", None):  # PYTORCH_CUDA_ALLOC_CONF
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:32'

if not os.environ.get("VLLM_WORKER_MULTIPROC_METHOD", None):  # VLLM_WORKER_MULTIPROC_METHOD
    os.environ['VLLM_WORKER_MULTIPROC_METHOD'] = 'spawn'

def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    if val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    raise ValueError(f"invalid truth value {val!r}")

# CFG
CFG = {}
# CFG SERVICE
CFG["SERVICE"] = {
    "NAME": "nvidia-common-infer-svc",
    "VERSION": "0.1.0",
    "FRAMEWORK": "fastapi",
    "HOST": "0.0.0.0",
    "PORT": 8899,
    "PROCESS_NUM": 1,
}
# CFG LOG
CFG["LOG"] = {
    "LOG_LEVEL": "INFO",
    "SLOW_RESPONSE": 10000
}
CFG["LLM"] = {
    "GC": True,
    "AUTH": "",
    "MODEL_NAME": "Common-Model",
    "DEVICE": "cuda" if torch.cuda.is_available() else "cpu",
    "MODEL_PATH": "/model",
    "MODEL_PRECISION": "bfloat16",  # float16, float32, bfloat16
    # function call
    "FNCALL_ENABLE": False,
    "FNCALL_TYPE": "qwen2",  # qwen qwen2 glm4
    # vllm
    "TENSOR_PARALLEL_SIZE": 1,
    "ENABLE_CHUNKED_PREFILL": None,
    "DEFAULT_MAX_NUM_SEQS": 20,
    "DEFAULT_GPU_MEMORY_UTILIZATION": 0.95,
    "DEFAULT_MAX_NUM_BATCHED_TOKENS": None,  # 默认等于DEFAULT_MAX_LENGTH
    # llm params
    "ADD_DEFAULT_SYSTEM_ROLE": True,
    "DEFAULT_DO_SAMPLE": True,
    "DEFAULT_TEMPERATURE": 1.0,
    "DEFAULT_TOPP": 1.0,
    "DEFAULT_TOPK": 20,
    "DEFAULT_REPETITION_PENALTY": 1.0,
    "DEFAULT_FREQUENCY_PENALTY": 0.0,
    "DEFAULT_PRESENCE_PENALTY": 0.0,
    "DEFAULT_MAX_LENGTH": 8192,  # 8k
    "DEFAULT_MAX_TOKEN": 2048,  # 2k
    "DEFAULT_BEAMS": 1,
}

# CFG SERVICE
if os.environ.get("SERVICE_NAME", None):
    CFG["SERVICE"]["NAME"] = os.environ.get("SERVICE_NAME")

if os.environ.get("SERVICE_VERSION", None):
    CFG["SERVICE"]["VERSION"] = os.environ.get("SERVICE_VERSION")

if os.environ.get("HTTP_HOST", None):
    CFG["SERVICE"]["HOST"] = os.environ.get("HTTP_HOST")

if os.environ.get("HTTP_PORT", None):
    CFG["SERVICE"]["PORT"] = int(os.environ.get("HTTP_PORT"))

if os.environ.get("PROCESS_NUM", None):
    CFG["SERVICE"]["PROCESS_NUM"] = int(os.environ.get("PROCESS_NUM"))

# CFG LOG
if os.environ.get("LOG_LEVEL", None):
    CFG["LOG"]["LOG_LEVEL"] = os.environ.get("LOG_LEVEL")

if os.environ.get("SLOW_RESPONSE", None):
    CFG["LOG"]["SLOW_RESPONSE"] = int(os.environ.get("SLOW_RESPONSE"))

# CFG LLM
if os.environ.get("GC", None):
    CFG["LLM"]["GC"] = strtobool(os.environ.get("GC"))

if os.environ.get("AUTH", None):
    CFG["LLM"]["AUTH"] = os.environ.get("AUTH")

if os.environ.get("MODEL_NAME", None):
    CFG["LLM"]["MODEL_NAME"] = os.environ.get("MODEL_NAME")

if os.environ.get("MODEL_PATH", None):
    CFG["LLM"]["MODEL_PATH"] = os.environ.get("MODEL_PATH")

if os.environ.get("MODEL_PRECISION", None):
    CFG["LLM"]["MODEL_PRECISION"] = os.environ.get("MODEL_PRECISION")

# function call
if os.environ.get("FNCALL_ENABLE", None):
    CFG["LLM"]["FNCALL_ENABLE"] = bool(strtobool(os.environ.get("FNCALL_ENABLE")))

if os.environ.get("FNCALL_TYPE", None):
    CFG["LLM"]["FNCALL_TYPE"] = os.environ.get("FNCALL_TYPE")

# llm params
if os.environ.get("ADD_DEFAULT_SYSTEM_ROLE", None):
    CFG["LLM"]["ADD_DEFAULT_SYSTEM_ROLE"] = bool(strtobool(os.environ.get("ADD_DEFAULT_SYSTEM_ROLE")))

if os.environ.get("DEFAULT_DO_SAMPLE", None):
    CFG["LLM"]["DEFAULT_DO_SAMPLE"] = bool(strtobool(os.environ.get("DEFAULT_DO_SAMPLE")))

if os.environ.get("DEFAULT_TEMPERATURE", None):
    CFG["LLM"]["DEFAULT_TEMPERATURE"] = float(os.environ.get("DEFAULT_TEMPERATURE"))

if os.environ.get("DEFAULT_TOPP", None):
    CFG["LLM"]["DEFAULT_TOPP"] = float(os.environ.get("DEFAULT_TOPP"))

if os.environ.get("DEFAULT_TOPK", None):
    CFG["LLM"]["DEFAULT_TOPK"] = int(os.environ.get("DEFAULT_TOPK"))

if os.environ.get("DEFAULT_REPETITION_PENALTY", None):
    CFG["LLM"]["DEFAULT_REPETITION_PENALTY"] = float(os.environ.get("DEFAULT_REPETITION_PENALTY"))

if os.environ.get("DEFAULT_FREQUENCY_PENALTY", None):
    CFG["LLM"]["DEFAULT_FREQUENCY_PENALTY"] = float(os.environ.get("DEFAULT_FREQUENCY_PENALTY"))

if os.environ.get("DEFAULT_PRESENCE_PENALTY", None):
    CFG["LLM"]["DEFAULT_PRESENCE_PENALTY"] = float(os.environ.get("DEFAULT_PRESENCE_PENALTY"))

if os.environ.get("DEFAULT_MAX_LENGTH", None):
    CFG["LLM"]["DEFAULT_MAX_LENGTH"] = int(os.environ.get("DEFAULT_MAX_LENGTH"))

if os.environ.get("DEFAULT_MAX_TOKEN", None):
    CFG["LLM"]["DEFAULT_MAX_TOKEN"] = int(os.environ.get("DEFAULT_MAX_TOKEN"))

if os.environ.get("DEFAULT_BEAMS", None):
    CFG["LLM"]["DEFAULT_BEAMS"] = int(os.environ.get("DEFAULT_BEAMS"))

# vllm
if os.environ.get("TENSOR_PARALLEL_SIZE", None):
    CFG["LLM"]["TENSOR_PARALLEL_SIZE"] = int(os.environ.get("TENSOR_PARALLEL_SIZE"))

if os.environ.get("ENABLE_CHUNKED_PREFILL", None):
    CFG["LLM"]["ENABLE_CHUNKED_PREFILL"] = bool(strtobool(os.environ.get("ENABLE_CHUNKED_PREFILL")))

if os.environ.get("DEFAULT_MAX_NUM_SEQS", None):
    CFG["LLM"]["DEFAULT_MAX_NUM_SEQS"] = int(os.environ.get("DEFAULT_MAX_NUM_SEQS"))

if os.environ.get("DEFAULT_GPU_MEMORY_UTILIZATION", None):
    CFG["LLM"]["DEFAULT_GPU_MEMORY_UTILIZATION"] = float(os.environ.get("DEFAULT_GPU_MEMORY_UTILIZATION"))

if os.environ.get("DEFAULT_MAX_NUM_BATCHED_TOKENS", None):
    CFG["LLM"]["DEFAULT_MAX_NUM_BATCHED_TOKENS"] = int(os.environ.get("DEFAULT_MAX_NUM_BATCHED_TOKENS"))
else:
    # 要求DEFAULT_MAX_LENGTH先被更新
    CFG["LLM"]["DEFAULT_MAX_NUM_BATCHED_TOKENS"] = CFG["LLM"]["DEFAULT_MAX_LENGTH"]

LOCK_PATH = f'/tmp/{CFG["SERVICE"]["NAME"]}'
if not os.path.exists(LOCK_PATH) or not os.path.isdir(LOCK_PATH):
    os.makedirs(LOCK_PATH, exist_ok=True)
    # logger.info("Init, service config: %s", CFG)

CFG = edict(CFG)
# logger.info("Init, load config success")
