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
Version route
"""
from fastapi import APIRouter

from telellm.config.config import CFG
from telellm.utils.rest_utils import make_response

router = APIRouter(
    tags=["version"],
)


@router.get("/version")
async def read_version():
    """
    Returns the version and configuration details of the system.
    """
    data = {
        "images_name": CFG.SERVICE.NAME,
        "images_version": CFG.SERVICE.VERSION,
        "device": CFG.LLM.DEVICE,
        "model_precision": CFG.LLM.MODEL_PRECISION,
        "temperature": CFG.LLM.DEFAULT_TEMPERATURE,
        "topp": CFG.LLM.DEFAULT_TOPP,
        "topk": CFG.LLM.DEFAULT_TOPK,
        "repetition_penalty": CFG.LLM.DEFAULT_REPETITION_PENALTY,
        "do_sample": CFG.LLM.DEFAULT_DO_SAMPLE,
        "max_tokens": CFG.LLM.DEFAULT_MAX_TOKEN,
        "max_length": CFG.LLM.DEFAULT_MAX_LENGTH,
        "model_path": CFG.LLM.MODEL_PATH
    }
    return make_response(data=data)
