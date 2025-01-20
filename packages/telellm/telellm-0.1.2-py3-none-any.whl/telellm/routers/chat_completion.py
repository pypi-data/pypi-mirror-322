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
LLM route
"""
import logging
import time
from typing import Union
from uuid import uuid4
from fastapi import APIRouter, Request, Response
from sse_starlette.sse import EventSourceResponse
from starlette.responses import JSONResponse
from telellm.check.chat_checker import check_parameters, check_inputs
from telellm.config.config import CFG
from telellm.infer.chat_infer import generate_stream, generate_text, get_prompt_inputs
from telellm.models.chat_model import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionStreamResponse
)
from telellm.status.status_exception import StatusException
from telellm.utils.rest_utils import make_exception_response


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1",
    tags=["llm"]
)


@router.post('/chat/completions', response_model=Union[ChatCompletionResponse, ChatCompletionStreamResponse])
async def create_chat_completion(req: Request, resp: Response, payload: ChatCompletionRequest):
    """Handles a chat completion request, validates input parameters, and generates and returns a chat response, 
    supporting both streaming and single-shot responses."""
    req_st = time.time()
    # reqid
    reqid = (
        req.headers["x-request-id"] if "x-request-id" in req.headers else uuid4().hex
    )
    resp.headers["x-request-id"] = reqid

    try:
        params = await check_parameters(reqid, payload)
        get_prompt_inputs(reqid, params)  # inputs, prompt_tokens
        check_inputs(reqid, params)
    except StatusException as e:
        data = make_exception_response(e.code, e.message, e.details)
        return JSONResponse(content=data, status_code=400)

    if payload.stream:
        generator = generate_stream(reqid, params)
        return EventSourceResponse(generator, media_type='text/event-stream')

    generator = await generate_text(reqid, params)

    req_time = (time.time() - req_st) * 1000
    logger.info("Reqid: %s, request success in %s ms", reqid, req_time)
    if req_time > CFG.LOG.SLOW_RESPONSE:
        logger.warning(
            "Reqid: %s, response time exceeds %s ms", reqid, CFG.LOG.SLOW_RESPONSE
        )

    return generator
