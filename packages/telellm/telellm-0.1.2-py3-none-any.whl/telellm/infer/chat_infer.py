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
"""chat_infer"""
# -*- coding:utf-8 -*-
import asyncio
import json
import logging
import time
import os
from pydantic import BaseModel
from transformers import AutoConfig

from telellm.config.config import CFG
from telellm.fncall.base_fncall_prompt import BaseFnCallPrompt
from telellm.models.chat_model import (
    DeltaMessage,
    ChatMessage,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatCompletionStreamResponse,
    ChatCompletionResponseStreamChoice,
    UsageInfo,
)
from telellm.models.chat_model import FunctionCall, ToolCall
from telellm.utils.fastapi_utils import llm_gc
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from vllm.transformers_utils.tokenizer import get_tokenizer

logger = logging.getLogger(__name__)

# global variate
STOP_SEQ = []

# chat_template
chat_template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chat_template.json"))
with open(chat_template_path, 'r', encoding='utf-8') as f:
    chat_template_data = json.load(f)
    # template_name
    template_name = chat_template_data['models'][CFG.LLM.MODEL_NAME][0]
    chat_template = chat_template_data['chat_templates'][template_name]
    # stop words - deduplicate
    stop_word_list = chat_template_data['models'][CFG.LLM.MODEL_NAME][1]
    STOP_SEQ = list(set(stop_word_list + STOP_SEQ)) if stop_word_list else STOP_SEQ
logger.info("chat_template read success")


# torch_dtype and max_length
try:
    # torch_dtype
    model_config_path = f'{CFG.LLM.MODEL_PATH}/config.json'
    with open(model_config_path, 'r', encoding='utf-8') as f:
        model_config = json.load(f)
    if 'torch_dtype' in model_config and model_config['torch_dtype'] != CFG.LLM.MODEL_PRECISION:
        model_config['torch_dtype'] = CFG.LLM.MODEL_PRECISION
        with open(model_config_path, 'w', encoding='utf-8') as f:
            json.dump(model_config, f, ensure_ascii=False, indent=4)  # type: ignore
        logger.info("torch_dtype(%s) updated to %s", CFG.LLM.MODEL_PRECISION, model_config_path)

    # DEFAULT_MAX_LENGTH
    model_max_length = 8192
    if 'max_position_embeddings' in model_config:
        model_max_length = model_config['max_position_embeddings']
    elif 'max_sequence_length' in model_config:
        model_max_length = model_config['max_sequence_length']
    elif 'seq_length' in model_config:
        model_max_length = model_config['seq_length']
    if model_max_length < CFG.LLM.DEFAULT_MAX_LENGTH:
        CFG.LLM.DEFAULT_MAX_LENGTH = model_max_length
        logger.info("model max length(%s) updated to DEFAULT_MAX_LENGTH", model_max_length)
except Exception as ee:
    logger.info("torch_dtype(%s) updated to config.json error, %s", CFG.LLM.MODEL_PRECISION, ee)

# function call
fncall_enable = CFG.LLM.FNCALL_ENABLE
base_fncall_prompt = BaseFnCallPrompt()

# model and tokenizer init
# use vllm tokenizer same as transformers
tokenizer = get_tokenizer(CFG.LLM.MODEL_PATH, trust_remote_code=True)
config = AutoConfig.from_pretrained(CFG.LLM.MODEL_PATH, trust_remote_code=True)
logger.info("tokenizer = %s", tokenizer)
logger.info("LLM config = %s", config)

# load model
asargs = AsyncEngineArgs(CFG.LLM.MODEL_PATH)
asargs.worker_use_ray = False
asargs.engine_use_ray = False
asargs.tokenizer = CFG.LLM.MODEL_PATH
asargs.tensor_parallel_size = CFG.LLM.TENSOR_PARALLEL_SIZE
asargs.trust_remote_code = True
asargs.enable_chunked_prefill = CFG.LLM.ENABLE_CHUNKED_PREFILL  # 分块预填充, 默认为None
asargs.gpu_memory_utilization = CFG.LLM.DEFAULT_GPU_MEMORY_UTILIZATION  # 默认0.8
asargs.dtype = CFG.LLM.MODEL_PRECISION  # 默认bfloat16
asargs.max_num_seqs = CFG.LLM.DEFAULT_MAX_NUM_SEQS  # 默认batch最大20条样本
asargs.max_model_len = CFG.LLM.DEFAULT_MAX_LENGTH
asargs.max_num_batched_tokens = CFG.LLM.DEFAULT_MAX_NUM_BATCHED_TOKENS
# asargs.quantization = "gptq"
# 对bitsandbytes量化需要特殊处理, just for llama model
config = config.to_dict()
if "quantization_config" in config:
    if config["quantization_config"]["quant_method"]=="bitsandbytes":
        asargs.quantization="bitsandbytes"
        asargs.load_format="bitsandbytes"

model = AsyncLLMEngine.from_engine_args(asargs)
logger.info("model = %s", model)
logger.info("model init success")


# To work around that unpleasant leading-\n tokenization issue!
def add_extra_stop_words(stop_words):
    """
    The function `add_extra_stop_words` adds additional stop words to a set and returns a list of all
    stop words.
    """
    if stop_words:
        _stop_words = set(STOP_SEQ)
        for x in stop_words:
            _stop_words.add(x)
            s = x.lstrip('\n')
            if s and (s not in _stop_words):
                _stop_words.add(s)
        return list(_stop_words)
    return STOP_SEQ if STOP_SEQ else stop_words


def trim_stop_words(text, stop_words):
    """
    The function `trim_stop_words` removes any stop words from the input text.
    """
    if stop_words:
        for stop in stop_words:
            idx = text.find(stop)
            if idx != -1:
                text = text[:idx]
    return text


# 用户停止句匹配
def match_user_stop_words(text, stop_words):
    """
    The function `match_user_stop_words` checks if a given text ends with any of the stop words
    provided.
    """
    for stop_word in stop_words:
        if len(text) < len(stop_word):
            continue
        if text[-len(stop_word):] == stop_word:
            return True  # 命中停止句, 返回True
    return False


def parse_parameters(params):
    """
    The function `parse_parameters` sets default values for various parameters used in text generation
    based on a given input dictionary.
    """
    # 请根据模型推荐值修改默认值
    gen_kwargs = {}

    # frequency_penalty
    if params["frequency_penalty"] is None:
        params["frequency_penalty"] = CFG.LLM.DEFAULT_FREQUENCY_PENALTY
    gen_kwargs["frequency_penalty"] = params["frequency_penalty"]

    # max_tokens
    if params["max_tokens"] is None:
        params["max_tokens"] = CFG.LLM.DEFAULT_MAX_TOKEN  # 最大输出
    gen_kwargs["max_tokens"] = params["max_tokens"]

    # presence_penalty
    if params["presence_penalty"] is None:
        params["presence_penalty"] = CFG.LLM.DEFAULT_PRESENCE_PENALTY
    gen_kwargs["presence_penalty"] = params["presence_penalty"]

    # seed
    gen_kwargs["seed"] = params["seed"]

    # temperature
    if params["temperature"] is None:
        params["temperature"] = CFG.LLM.DEFAULT_TEMPERATURE
    gen_kwargs["temperature"] = params["temperature"]

    # top_k
    if params["top_k"] is None:
        params["top_k"] = CFG.LLM.DEFAULT_TOPK
    gen_kwargs["top_k"] = params["top_k"]
    if gen_kwargs["top_k"] == 1:
        gen_kwargs["temperature"] = 0  # 关闭随机性(vllm当temperature=0时有效)

    # top_p
    if params["top_p"] is None:
        params["top_p"] = CFG.LLM.DEFAULT_TOPP
    gen_kwargs["top_p"] = params["top_p"]

    # repetition_penalty
    if params["repetition_penalty"] is None:
        params["repetition_penalty"] = CFG.LLM.DEFAULT_REPETITION_PENALTY
    gen_kwargs["repetition_penalty"] = params["repetition_penalty"]

    return gen_kwargs


def get_prompt_inputs(reqid, params):
    """
    This function retrieves prompt inputs for a chatbot conversation based on the provided parameters.
    """

    # query, history, system = params["query"], params["history"], params["system"]
    # query
    print(f"query: {params['query']}")

    # tools/functions support
    if fncall_enable:
        params["messages"] = base_fncall_prompt.process_messages(
            params["messages"], params["tools"], params["functions"],
            params["tool_choice"], params["function_call"], params["parallel_tool_calls"], params["lang"]
        )

    conversation = params['messages']

    # 设置自定义template
    tokenizer.chat_template = chat_template

    # inputs
    prompt = tokenizer.apply_chat_template(
        conversation,
        tokenize=False,
        add_generation_prompt=True,
        return_tensors='pt',
    )

    prompt_token_ids = tokenizer.encode(prompt)
    prompt_tokens = len(prompt_token_ids)

    params['prompt'] = prompt
    params['prompt_token_ids'] = prompt_token_ids
    params['prompt_tokens'] = prompt_tokens

    logger.info("Reqid: %s, get_prompt_inputs, prompt_tokens: %s", reqid, prompt_tokens)


def _chat_stream(reqid, prompt, prompt_token_ids, gen_kwargs):
    # sampling_params
    sampling_params = SamplingParams(
        presence_penalty=gen_kwargs['presence_penalty'],
        frequency_penalty=gen_kwargs['frequency_penalty'],
        repetition_penalty=gen_kwargs['repetition_penalty'],
        temperature=gen_kwargs['temperature'],
        top_p=gen_kwargs['top_p'],
        top_k=gen_kwargs['top_k'],
        seed=gen_kwargs['seed'],
        stop=gen_kwargs['stop'],
        max_tokens=gen_kwargs['max_tokens'],
        skip_special_tokens=True
    )

    inputs = {
        "prompt": prompt,
        "prompt_token_ids": prompt_token_ids
    }

    # generate
    response_generator = model.generate(
        inputs,
        sampling_params=sampling_params,
        request_id=reqid,
    )

    return response_generator


async def generate_stream(reqid, params):
    """
    The `generate_stream` function generates a stream of chat completion
    responses based on input parameters and user interactions, including handling stop words,
    tool/function calls, and completion tokens.
    """

    # stop, gen_kwargs
    stop_words = add_extra_stop_words(params["stop"])
    gen_kwargs = parse_parameters(params)
    gen_kwargs['stop'] = stop_words
    logger.info("Reqid: %s, generate stream, stop_words: %s, generate_params: %s", reqid, stop_words, gen_kwargs)

    # params
    include_usage = params['include_usage']
    prompt = params['prompt']
    prompt_token_ids = params['prompt_token_ids']
    prompt_tokens = params['prompt_tokens']
    completion_tokens = 0

    # role
    choice_data = ChatCompletionResponseStreamChoice(
        index=0, delta=DeltaMessage(role='assistant'), finish_reason=None
    )
    chunk = ChatCompletionStreamResponse(
        id=f"chatcmpl-{str(reqid)}",
        created=int(time.time()),
        object="chat.completion.chunk",
        model=params["model"],
        choices=[choice_data],
    )
    if include_usage is not None and include_usage:
        chunk.usage = UsageInfo(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )
    yield f'{_dump_json(chunk, exclude_unset=True)}'

    # max_tokens revise
    if (CFG.LLM.DEFAULT_MAX_LENGTH - prompt_tokens) < gen_kwargs['max_tokens']:
        gen_kwargs['max_tokens'] = CFG.LLM.DEFAULT_MAX_LENGTH - prompt_tokens

    current_length = 0
    user_stop_words = set(stop_words) - set(STOP_SEQ)  # 用户输入的stop_words进行延迟
    delay_token_num = max(map(len, stop_words)) if user_stop_words else 0

    if fncall_enable:
        has_tool = params["tools"] or params["functions"]
        has_choice = params["tool_choice"] != "none" and params["function_call"] != "none"
        use_tool = has_tool and has_choice
    else:
        use_tool = False

    # response
    print("model: ")
    _new_response = ""
    async for output in _chat_stream(reqid, prompt, prompt_token_ids, gen_kwargs):
        _new_response = output.outputs[0].text
        completion_tokens = len(output.outputs[0].token_ids)

        # tool/function call
        if use_tool:
            print(_new_response[current_length:], end='', flush=True)
            current_length = len(_new_response)
            continue

        # delay
        if len(_new_response) <= delay_token_num:
            continue
        new_response = _new_response[:-delay_token_num] if delay_token_num != 0 else _new_response
        if len(new_response) == current_length:
            continue
        # new_text
        new_text = new_response[current_length:]
        current_length = len(new_response)
        # print
        print(new_text, end='', flush=True)
        # reply
        choice_data = ChatCompletionResponseStreamChoice(
            index=0, delta=DeltaMessage(content=new_text), finish_reason=None
        )
        chunk = ChatCompletionStreamResponse(
            id=f"chatcmpl-{str(reqid)}",
            created=int(time.time()),
            object="chat.completion.chunk",
            model=params["model"],
            choices=[choice_data],
        )
        if include_usage is not None and include_usage:
            chunk.usage = UsageInfo(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            )
        yield f'{_dump_json(chunk, exclude_unset=True)}'
        await asyncio.sleep(0.000001)
        if stop_words and match_user_stop_words(_new_response, stop_words):
            await model.abort(reqid)  # 终止vllm后续推理
            break

    # revise vllm tokens
    completion_tokens = len(tokenizer(_new_response, return_tensors='pt')['input_ids'][0])

    # tool/function call
    content = ""
    function_calls = None
    if use_tool:
        content, function_calls = base_fncall_prompt.process_response(
            _new_response, params["tools"], params["functions"],
            params["tool_choice"], params["function_call"], params["parallel_tool_calls"]
        )
        if function_calls is None:
            # it should be fncall, but the output is not
            current_length = 0

    # delayed_text
    if current_length != len(_new_response):
        # Determine whether to print the delay tokens
        delayed_text = _new_response[current_length:]
        new_text = trim_stop_words(delayed_text, stop_words)
        if len(new_text) > 0:
            # print
            print(new_text, end='', flush=True)

            choice_data = ChatCompletionResponseStreamChoice(
                index=0, delta=DeltaMessage(content=new_text), finish_reason=None
            )
            chunk = ChatCompletionStreamResponse(
                id=f"chatcmpl-{str(reqid)}",
                created=int(time.time()),
                object="chat.completion.chunk",
                model=params["model"],
                choices=[choice_data],
            )
            if include_usage is not None and include_usage:
                chunk.usage = UsageInfo(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens
                )
            yield f'{_dump_json(chunk, exclude_unset=True)}'

    finish_reason = 'length' if completion_tokens >= gen_kwargs['max_tokens'] else 'stop'
    # tool/function call
    if function_calls:
        tool_calls = []
        function_call = None
        function_calls = [
            FunctionCall(name=function["name"], arguments=function["arguments"]) for function in function_calls
        ]
        if params["tools"]:
            for function in function_calls:
                tool_calls.append(ToolCall(function=function))
                finish_reason = 'tool_calls'
        elif params["functions"]:
            if len(function_calls):
                function_call = function_calls[0]
                finish_reason = 'function_call'
        delta_message = DeltaMessage(
            **{k: v for k, v in
               {'content': content, 'function_call': function_call, 'tool_calls': tool_calls}.items()
               if v}
        )
        choice_data = ChatCompletionResponseStreamChoice(
            index=0, delta=delta_message, finish_reason=None
        )
        chunk = ChatCompletionStreamResponse(
            id=f"chatcmpl-{str(reqid)}",
            created=int(time.time()),
            object="chat.completion.chunk",
            model=params["model"],
            choices=[choice_data],
        )
        if include_usage is not None and include_usage:
            chunk.usage = UsageInfo(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            )
        yield f'{_dump_json(chunk, exclude_unset=True)}'

    # stop
    print(" [DONE]")
    choice_data = ChatCompletionResponseStreamChoice(
        index=0, delta=DeltaMessage(), finish_reason=finish_reason
    )
    chunk = ChatCompletionStreamResponse(
        id=f"chatcmpl-{str(reqid)}",
        created=int(time.time()),
        object="chat.completion.chunk",
        model=params["model"],
        choices=[choice_data],
    )
    if include_usage is not None and include_usage:
        chunk.usage = UsageInfo(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )
    yield f'{_dump_json(chunk, exclude_unset=True)}'

    yield '[DONE]'

    llm_gc()


async def generate_text(reqid, params):
    """
    The function `generate_text` processes input parameters, generates text output based on a prompt,
    handles stop words, and supports tool and function calls.
    """

    # stop, gen_kwargs
    stop_words = add_extra_stop_words(params["stop"])
    gen_kwargs = parse_parameters(params)
    gen_kwargs['stop'] = stop_words
    logger.info("Reqid: %s, generate text, stop_words: %s, generate_params: %s", reqid, stop_words, gen_kwargs)

    # params
    prompt = params['prompt']
    prompt_token_ids = params['prompt_token_ids']
    prompt_tokens = params['prompt_tokens']

    # max_tokens revise
    if (CFG.LLM.DEFAULT_MAX_LENGTH - prompt_tokens) < gen_kwargs['max_tokens']:
        gen_kwargs['max_tokens'] = CFG.LLM.DEFAULT_MAX_LENGTH - prompt_tokens

    # response
    response = ""
    async for output in _chat_stream(reqid, prompt, prompt_token_ids, gen_kwargs):
        response = output.outputs[0].text
        if stop_words and match_user_stop_words(response, stop_words):
            await model.abort(reqid)  # 终止vllm后续推理
            break

    # revise vllm tokens
    completion_tokens = len(tokenizer(response, return_tensors='pt')['input_ids'][0])

    content = trim_stop_words(response, stop_words)

    print(f"model: {content}")

    # finish_reason
    finish_reason = 'length' if completion_tokens >= gen_kwargs['max_tokens'] else 'stop'

    # tool/function call support
    tool_calls = []
    function_call = None
    if fncall_enable:
        content, function_calls = base_fncall_prompt.process_response(
            content, params["tools"], params["functions"],
            params["tool_choice"], params["function_call"], params["parallel_tool_calls"]
        )
        if function_calls:
            function_calls = [
                FunctionCall(name=function["name"], arguments=function["arguments"]) for function in function_calls
            ]
            if params["tools"]:
                for function in function_calls:
                    tool_calls.append(ToolCall(function=function))
                    finish_reason = 'tool_calls'
            elif params["functions"]:
                if function_calls:
                    function_call = function_calls[0]
                    finish_reason = 'function_call'

    choice_data = ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role='assistant', content=content, function_call=function_call, tool_calls=tool_calls),
        finish_reason=finish_reason
    )
    chunk = ChatCompletionResponse(
        id=f"chatcmpl-{str(reqid)}",
        model=params["model"],
        choices=[choice_data],
        usage=UsageInfo(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )
    )

    llm_gc()

    return chunk


def _dump_json(data: BaseModel, *args, **kwargs) -> str:
    try:
        return data.model_dump_json(*args, **kwargs)
    except AttributeError:  # pydantic<2.0.0
        return data.json(*args, **kwargs)  # noqa
