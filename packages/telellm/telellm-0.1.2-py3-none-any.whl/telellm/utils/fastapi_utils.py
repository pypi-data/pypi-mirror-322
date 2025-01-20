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
"""fastapi_utils"""
# -*- encoding: utf-8 -*-
from contextlib import asynccontextmanager
import gc
import torch
from pydantic import BaseModel, Field
from fastapi import FastAPI
from telellm.config.config import CFG
from telellm.status.http_status import HTTPStatus

def llm_gc(forced: bool = False):
    """Clears garbage collection and GPU memory cache if enabled or forced, based on configuration settings."""
    if not CFG.LLM.GC and not forced:
        return
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


@asynccontextmanager
async def lifespan(app: FastAPI):  # collects GPU memory
    """
    Handles GPU memory cleanup at the end of the application lifespan.
    """
    yield
    llm_gc(forced=True)


class SuccessResult(BaseModel):
    """SuccessResult"""
    pass


class ApiServerBaseResponse(BaseModel):
    """
    Base response model for API server, containing a status code.
    """
    code: int = Field(HTTPStatus.SUCCESS.value, description="状态码")


class ApiServerFailedResponse(ApiServerBaseResponse):
    """
    Response model for API server when the request fails, including a failure status code,
    error message, and details about the failure.
    """
    code: int = Field(HTTPStatus.SERVER_ERR.value, description="状态码")
    message: str = Field(HTTPStatus.SERVER_ERR.message, description="错误信息")
    details: str = Field(HTTPStatus.SERVER_ERR.details, description="详细的错误信息")
