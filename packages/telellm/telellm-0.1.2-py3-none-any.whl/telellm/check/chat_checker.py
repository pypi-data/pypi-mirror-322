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
"""chat_checker"""
import logging
import re
from typing import List, Dict, Tuple

from telellm.config.config import CFG
from telellm.models.chat_model import ChatCompletionRequest
from telellm.status.http_status import HTTPStatus
from telellm.status.status_exception import StatusException

logger = logging.getLogger(__name__)


# get messages language
def get_messages_lang(messages):
    """
    Determines the language of a list of messages by checking for the presence of Chinese characters in the content.
    """
    chinese_char_re = re.compile(r'[\u4e00-\u9fff]')

    def has_chinese_chars(data) -> bool:
        text = f'{data}'
        return bool(chinese_char_re.search(text))

    def has_chinese_messages(_messages, check_roles: Tuple[str] = ("system", "user")) -> bool:
        for m in _messages:
            if m['role'] in check_roles:
                if has_chinese_chars(m['content']):
                    return True
        return False

    lang = 'zh' if has_chinese_messages(messages) else 'en'
    return lang


# messages check
async def check_messages(reqid, messages):
    """
    The function `check_messages` processes a list of messages based on their roles and content,
    following a state machine logic to ensure proper message sequencing.
    """
    conversation: List[Dict] = []

    # except start system
    state = "system"
    for _, msg in enumerate(messages):
        role, content = msg["role"], msg.get("content", '')

        # content handle
        content = content.lstrip('\n').rstrip()
        if not content and role == "user":
            logger.info("reqid: %s, messages value err, role: %s, content value should not empty.", reqid, role)
            raise StatusException(HTTPStatus.VALUE_ERR,
                                  custom_details=f"messages 字段值不符合规范，{role}的content值不能为空")

        # parse parameter using state machine
        if state == "system":
            if CFG.LLM.ADD_DEFAULT_SYSTEM_ROLE:
                system = 'You are a helpful assistant.'
                if role == "system":
                    if content.strip():
                        system = content.strip()
                conversation.append({"role": state, "content": system})
            state = "user"
            if role == "user":
                conversation.append({"role": role, "content": content})
                state = "assistant"
            if role == "assistant":
                logger.info(
                    "reqid: %s, messages value err, expected 'user' or 'system' first, but found 'assistant'.", reqid)  # noqa
                raise StatusException(HTTPStatus.VALUE_ERR, custom_details="messages 字段值不符合规范，期望首先是'user'/'system'，但输入为'assistant'")  # noqa
        elif state == "user":
            # user/function/tool
            if role == "user":
                conversation.append({"role": role, "content": content})
            elif role == "function":
                name = msg.get("name", '')  # Function message Required
                if not name.rstrip():
                    logger.info(
                        "reqid: %s, messages value err, expected 'name' in 'function' message but found empty.", reqid)  # noqa
                    raise StatusException(HTTPStatus.VALUE_ERR, custom_details="messages 字段值不符合规范，function的name值不能为空")  # noqa
                conversation.append({"role": role, "content": content, "name": name})
            elif role == "tool":
                tool_call_id = msg.get("tool_call_id", '')  # Tool message Required
                if not tool_call_id.rstrip():
                    logger.info(
                        "reqid: %s, messages value err, expected 'tool_call_id' in 'tool' message but found empty.", reqid)  # noqa
                    raise StatusException(HTTPStatus.VALUE_ERR, custom_details="messages 字段值不符合规范，tool中的tool_call_id值不能为空")  # noqa
                conversation.append({"role": role, "content": content, "tool_call_id": tool_call_id})
            else:
                logger.info(
                    "reqid: %s, messages value err, expected 'user' or 'function' or 'tool' after 'system' or \
                    'assistant', but found: '%s'.", reqid, role)  # noqa
                raise StatusException(HTTPStatus.VALUE_ERR, custom_details="messages 字段值不符合规范，system/assistant后应该是user/function/tool")  # noqa
            state = "assistant"
        elif state == "assistant":
            # assistant: tool_calls/function_call
            if role == "assistant":
                tool_calls = msg.get("tool_calls", None)
                function_call = msg.get("function_call", None)
                # Required unless tool_calls or function_call is specified
                if not tool_calls and not function_call and not content:
                    logger.info("reqid: %s, messages value err, role: %s, content value should not empty.", reqid, role)
                    raise StatusException(HTTPStatus.VALUE_ERR, custom_details=f"messages 字段值不符合规范，{role}的content值不能为空")  # noqa
                if tool_calls:
                    conversation.append({"role": role, "content": content, "tool_calls": tool_calls})
                elif function_call:
                    conversation.append({"role": role, "content": content, "function_call": function_call})
                else:
                    conversation.append({"role": role, "content": content})
                state = "user"
            else:
                logger.info(
                    "reqid: %s, messages value err, expected 'assistant' after 'user'/'function'/'tool', but found: '%s'.", reqid, role)  # noqa
                raise StatusException(HTTPStatus.VALUE_ERR, custom_details="messages 字段值不符合规范，user/function/tool后应该是assistant")  # noqa

    if state != "assistant":
        logger.info(
            "reqid: %s, messages value err, the last message role must user, but %s.", reqid, conversation[-1]['role'])  # noqa
        raise StatusException(HTTPStatus.VALUE_ERR, custom_details=f"messages 字段值不符合规范，最后一个message的角色必须是 \
                              user/function/tool，输入为{conversation[-1]['role']}")  # noqa

    return conversation


def remove_fncall_messages(messages, lang):
    """Change function calls into user messages so that the model won't try to generate function calls when given functions and function_choice="none"."""
    # Change function calls into user messages so that the model won't try
    # to generate function calls when given functions and function_choice="none".
    new_messages = []
    for msg in messages:
        function_call = msg.get("function_call", None)
        tool_calls = msg.get("tool_calls", None)
        if (msg["role"] == "function") or function_call or \
                (msg["role"] == "tool") or (tool_calls and tool_calls[0]):
            # init
            if (not new_messages) or (new_messages[-1]["role"] != "user"):
                new_messages.append({"role": "user", "content": ""})
            # function_call or tool_calls
            if function_call or (tool_calls and tool_calls[0]):
                tool_name, tool_args = "", ""
                if function_call:
                    tool_name = function_call.name
                    tool_args = function_call.arguments
                if tool_calls and tool_calls[0]:
                    tool_name = tool_calls[0].function.name
                    tool_args = tool_calls[0].function.arguments
                if lang == 'zh':
                    tool_text = f'\n\n工具"{tool_name}"被调用时使用了以下参数：\n{tool_args}'
                else:
                    tool_text = f'\n\nThe tool "{tool_name}" was called with these arguments:\n{tool_args}'
            else:
                # role="function" or role="tool"
                if msg["content"]:
                    tool_result = msg["content"]
                else:
                    tool_result = 'No result.'
                if lang == 'zh':
                    tool_text = f'\n\n该工具返回了以下结果：\n{tool_result}'
                else:
                    tool_text = f'\n\nThe tool has returned the following result:\n{tool_result}'
            new_messages[-1]["content"] += tool_text
        else:
            if (msg["role"] == "user") and new_messages and (new_messages[-1]["role"] == "user"):
                # Separate two user messages with an assistant message to make the bot focus on the latter:
                new_messages.append({"role": "assistant", "content": "..."})
            new_messages.append(msg)
    return new_messages


# parameters check
async def check_parameters(reqid, payload: ChatCompletionRequest):
    """
    The function `check_parameters` in Python performs parameter validation for a ChatCompletionRequest
    payload and returns a dictionary of validated parameters.
    """
    params = {}

    # model(必选)
    if not payload.model:
        logger.info("reqid: %s, model empty err.", reqid)
        raise StatusException(HTTPStatus.CUSTOMIZE_EMPTY_ERR, custom_field="model")
    params["model"] = payload.model

    # messages(必选) --- support tool/function call
    if not payload.messages:
        logger.info("reqid: %s, messages empty err.", reqid)
        raise StatusException(HTTPStatus.CUSTOMIZE_EMPTY_ERR, custom_field="messages")
    conversation = await check_messages(reqid, payload.messages)
    params["messages"] = conversation

    # messages language
    params["lang"] = get_messages_lang(params["messages"])

    # tool_choice(可选) and function_call(可选)
    params["tool_choice"] = payload.tool_choice
    params["function_call"] = payload.function_call

    # function call init
    functions_mode = False  # 是否开启function call / tool call
    params["parallel_tool_calls"] = False  # 仅tools支持parallel_tool_calls
    params["tools"] = None  # noqa
    params["functions"] = None  # noqa

    # tools(可选)
    if payload.tools is not None:
        if len(payload.tools) < 1:
            logger.info("reqid: %s, tools empty err.", reqid)
            raise StatusException(HTTPStatus.CUSTOMIZE_EMPTY_ERR, custom_field="tools")
        valid_fn_choices = [f.function.name for f in payload.tools]
        valid_fn_choices = ['auto', 'none'] + valid_fn_choices
        # tool_choice
        if isinstance(payload.tool_choice, str):
            fn_choice = payload.tool_choice
        else:
            fn_choice = payload.tool_choice.function.name  # noqa
        if fn_choice not in valid_fn_choices:
            logger.info("reqid: %s, tool_choice value err, the value of tool_choice must be one of the \
                        following: %s, but %s is received.", reqid, valid_fn_choices, fn_choice)

            raise StatusException(HTTPStatus.VALUE_ERR, custom_field="tool_choice")
        if payload.tool_choice != "none":
            params["tools"] = payload.tools
            # parallel_tool_calls(可选)
            params["parallel_tool_calls"] = payload.parallel_tool_calls
            functions_mode = True

    # functions(可选)
    if payload.functions is not None and not functions_mode:
        if len(payload.functions) < 1:
            logger.info("reqid: %s, functions empty err.", reqid)
            raise StatusException(HTTPStatus.CUSTOMIZE_EMPTY_ERR, custom_field="functions")
        valid_fn_choices = [f.name for f in payload.functions]
        valid_fn_choices = ['auto', 'none'] + valid_fn_choices
        # function_call
        if isinstance(payload.function_call, str):
            fn_choice = payload.function_call
        else:
            fn_choice = payload.function_call.name  # noqa
        if fn_choice not in valid_fn_choices:
            logger.info("reqid: %s, function_call value err, the value of function_call must be one of the \
                        following: %s, but %s is received.", reqid, valid_fn_choices, fn_choice)

            raise StatusException(HTTPStatus.VALUE_ERR, custom_field="function_call")
        if payload.function_call != "none":
            params["functions"] = payload.functions
            functions_mode = True
    logger.info("reqid: %s, functions_mode: %s", reqid, functions_mode)

    if not functions_mode:
        # remove function_call or tool_calls
        params["messages"] = remove_fncall_messages(params["messages"], params["lang"])

    # system query history
    params["system"] = params["messages"][0]["content"]
    params["history"] = params["messages"][1:-1]
    params["query"] = params["messages"][-1]["content"]

    # frequency_penalty(可选) [-2, 2]
    if payload.frequency_penalty is not None:
        if payload.frequency_penalty < -2. or payload.frequency_penalty > 2.:
            logger.info("reqid: %s, frequency_penalty value err, %s not in [-2, 2]", reqid, payload.frequency_penalty)
            raise StatusException(HTTPStatus.VALUE_ERR, custom_details="frequency_penalty 字段值应该在[-2, 2]")
    params["frequency_penalty"] = payload.frequency_penalty

    # max_tokens(可选) (0, DEFAULT_MAX_TOKEN]
    if payload.max_tokens is not None:
        if payload.max_tokens <= 0 or payload.max_tokens > CFG.LLM.DEFAULT_MAX_TOKEN:
            logger.info(
                "reqid: %s, max_tokens value err, %s not in (0, %s]", reqid, payload.max_tokens, CFG.LLM.DEFAULT_MAX_TOKEN
            )

            raise StatusException(HTTPStatus.VALUE_ERR, custom_details=f"max_tokens 字段值应该在(0, {CFG.LLM.DEFAULT_MAX_TOKEN}]")  # noqa
    params["max_tokens"] = payload.max_tokens

    # presence_penalty(可选) [-2, 2]
    if payload.presence_penalty is not None:
        if payload.presence_penalty < -2. or payload.presence_penalty > 2.:
            logger.info("reqid: %s, presence_penalty value err, %s not in [-2, 2]", reqid, payload.presence_penalty)
            raise StatusException(HTTPStatus.VALUE_ERR, custom_details="presence_penalty 字段值应该在[-2, 2]")
    params["presence_penalty"] = payload.presence_penalty

    # seed(可选) (0, 9223372036854775807]
    if payload.seed is not None:
        if payload.seed <= 0 or payload.seed > 9223372036854775807:
            logger.info("reqid: %s, seed value err, %s not in (0, 9223372036854775807]", reqid, payload.seed)
            raise StatusException(HTTPStatus.VALUE_ERR, custom_details="seed 字段值应该在(0, 9223372036854775807]")
    params["seed"] = payload.seed

    # stop(可选) -- 不能有空字符
    if isinstance(payload.stop, str):
        params["stop"] = [payload.stop]
    else:
        params["stop"] = payload.stop
    for s in params["stop"]:
        if not s:
            logger.info("reqid: %s, stop value err, %s cannot contain an empty string", reqid, payload.stop)
            raise StatusException(HTTPStatus.VALUE_ERR, custom_details="stop 字段值不能包含空字符串")

    # stream(可选) ---无需校验
    params["stream"] = payload.stream

    # stream_options(可选) ---无需校验
    if payload.stream_options is not None:
        params["include_usage"] = payload.stream_options.include_usage
    else:
        params["include_usage"] = None

    # temperature(可选) (0, 2)
    if payload.temperature is not None:
        if payload.temperature <= 0. or payload.temperature >= 2.:
            logger.info("reqid: %s, temperature value err, %s not in (0, 2.0)", reqid, payload.temperature)
            raise StatusException(HTTPStatus.VALUE_ERR, custom_details="temperature 字段值应该在(0, 2.0)")
    params["temperature"] = payload.temperature

    # top_p(可选) (0, 1.0]
    if payload.top_p is not None:
        if payload.top_p <= 0. or payload.top_p > 1.:
            logger.info("reqid: %s, top_p value err, %s not in (0, 1.0]", reqid, payload.top_p)
            raise StatusException(HTTPStatus.VALUE_ERR, custom_details="top_p 字段值应该在(0, 1.0]")
    params["top_p"] = payload.top_p

    # top_k(可选) [1, 100]
    if payload.top_k is not None:
        if payload.top_k < 1 or payload.top_k > 100:
            logger.info("reqid: %s, top_k value err, %s not in [1, 100]", reqid, payload.top_k)
            raise StatusException(HTTPStatus.VALUE_ERR, custom_details="top_k 字段值应该在[1, 100]")
    params["top_k"] = payload.top_k

    # repetition_penalty(可选) (0, 2)
    if payload.repetition_penalty is not None:
        if payload.repetition_penalty <= 0 or payload.repetition_penalty >= 2:
            logger.info("reqid: %s, repetition_penalty value err, %s not in (0, 2)", reqid, payload.repetition_penalty)
            raise StatusException(HTTPStatus.VALUE_ERR, custom_details="repetition_penalty 字段值应该在(0, 2)")
    params["repetition_penalty"] = payload.repetition_penalty

    return params


# inputs check
def check_inputs(reqid, params):
    """
    The function `check_inputs` checks if the input text length exceeds a predefined maximum length and
    raises an exception if it does.
    """
    prompt_tokens = params['prompt_tokens']

    if prompt_tokens >= CFG.LLM.DEFAULT_MAX_LENGTH:
        logger.info(
            "reqid: %s, input text is too long, prompt_tokens(%s) >= DEFAULT_MAX_LENGTH(%s)",
            reqid, prompt_tokens, CFG.LLM.DEFAULT_MAX_LENGTH
        )

        raise StatusException(HTTPStatus.VALUE_ERR, custom_details="messages 字段值文本已超过最大上下文")
