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
"""chat_model"""
import time
import uuid
from typing import Dict, List, Literal, Optional, Union, Any

import openai.types.chat
from pydantic import ConfigDict, Field
from typing_extensions import TypedDict, Required
from telellm.models.model import OpenAIBaseModel


# --------------------base class--------------
def random_uuid() -> str:
    """The function `random_uuid` generates a random UUID and returns it as a string."""
    return str(uuid.uuid4().hex)


class ResponseFormat(OpenAIBaseModel):
    """The class `ResponseFormat` defines a type attribute that must be either "text" or "json_object"."""
    # type must be "json_object" or "text"
    type: Literal["text", "json_object"]


class StreamOptions(OpenAIBaseModel):
    """The `StreamOptions` class includes an optional boolean attribute `include_usage`."""
    include_usage: Optional[bool]


class FunctionDefinition(OpenAIBaseModel):
    """The `FunctionDefinition` class in Python represents a function definition with a name, optional
       description, and optional parameters."""
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class ChatCompletionToolsParam(OpenAIBaseModel):
    """The `ChatCompletionToolsParam` class in Python represents a parameter for chat completion tools with
       a type of "function" and a function definition attribute."""
    type: Literal["function"] = "function"
    function: FunctionDefinition


class ChatCompletionNamedFunction(OpenAIBaseModel):
    """The class `ChatCompletionNamedFunction` in Python represents a named function for chat completion."""
    name: str


class ChatCompletionNamedToolChoiceParam(OpenAIBaseModel):
    """This class defines a parameter for choosing a named function in a chat completion tool."""
    function: ChatCompletionNamedFunction
    type: Literal["function"] = "function"


class ChatCompletionLogProb(OpenAIBaseModel):
    """This Python class `ChatCompletionLogProb` defines a data structure with attributes for a token, log
       probability, and optional byte list."""
    token: str
    logprob: float = -9999.0
    bytes: Optional[List[int]] = None


class ChatCompletionLogProbsContent(ChatCompletionLogProb):
    """The class `ChatCompletionLogProbsContent` contains a list of `ChatCompletionLogProb` objects stored
       in the `top_logprobs` attribute."""
    top_logprobs: List[ChatCompletionLogProb] = Field(default_factory=list)


class ChatCompletionLogProbs(OpenAIBaseModel):
    """The `ChatCompletionLogProbs` class includes an optional list of
       `ChatCompletionLogProbsContent` objects for chat completion log probabilities."""
    content: Optional[List[ChatCompletionLogProbsContent]] = None


class UsageInfo(OpenAIBaseModel):
    """The `UsageInfo` class defines attributes related to token usage for a model."""
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0


class FunctionCall(OpenAIBaseModel):
    """The `FunctionCall` class represents a function call with a name and arguments."""
    name: str
    arguments: str


class ToolCall(OpenAIBaseModel):
    """The `ToolCall` class defines a tool call with an ID, type, and function call."""
    id: str = Field(default_factory=lambda: f"chatcmpl-tool-{random_uuid()}")
    type: Literal["function"] = "function"
    function: FunctionCall


class ChatMessage(OpenAIBaseModel):
    """The `ChatMessage` class represents a message in a chat with a role, content, function call, and tool
       calls."""
    role: Literal['user', 'assistant', 'system', 'function', 'tool']
    content: Optional[str]
    function_call: Optional[FunctionCall] = None
    tool_calls: List[ToolCall] = Field(default_factory=list)


class CustomChatCompletionContentPartParam(TypedDict, total=False):
    """The class `CustomChatCompletionContentPartParam` defines a data structure with a required `type`
       field representing the type of the content part."""
    __pydantic_config__ = ConfigDict(extra="allow")  # type: ignore

    type: Required[str]
    """The type of the content part."""


ChatCompletionContentPartParam = Union[
    openai.types.chat.ChatCompletionContentPartParam,
    CustomChatCompletionContentPartParam]


class CustomChatCompletionMessageParam(TypedDict, total=False):
    """Enables custom roles in the Chat Completion API."""
    role: Required[str]
    """The role of the message's author."""

    content: Union[str, List[ChatCompletionContentPartParam]]
    """The contents of the message."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the
    same role.
    """


ChatCompletionMessageParam = Union[
    openai.types.chat.ChatCompletionMessageParam,
    CustomChatCompletionMessageParam]


# --------------------ChatCompletionRequest--------------
class ChatCompletionRequest(OpenAIBaseModel):
    """The `ChatCompletionRequest` class defines parameters for generating chat completions using the
       OpenAI API."""
    # Ordered by official OpenAI API documentation
    # https://platform.openai.com/docs/api-reference/chat/create
    messages: List[ChatCompletionMessageParam]
    model: str
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[str, float]] = None
    logprobs: Optional[bool] = False
    top_logprobs: Optional[int] = 0
    max_tokens: Optional[int] = None
    n: Optional[int] = 1
    presence_penalty: Optional[float] = None
    response_format: Optional[ResponseFormat] = None
    seed: Optional[int] = None  # ge=torch.iinfo(torch.long).min/0 le=torch.iinfo(torch.long).max
    service_tier: Optional[str] = None
    stop: Optional[Union[str, List[str]]] = Field(default_factory=list)
    stream: Optional[bool] = False
    stream_options: Optional[StreamOptions] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None  # add
    repetition_penalty: Optional[float] = None  # add
    tools: Optional[List[ChatCompletionToolsParam]] = None
    tool_choice: Optional[Union[Literal["none", "auto", "required"], ChatCompletionNamedToolChoiceParam]] = "auto"
    parallel_tool_calls: Optional[bool] = True
    user: Optional[str] = None
    function_call: Optional[Union[Literal["none", "auto"],
                            ChatCompletionNamedFunction]] = "auto"  # Deprecated in favor of tool_choice
    functions: Optional[List[FunctionDefinition]] = None  # Deprecated in favor of tools


# --------------------ChatCompletionResponse--------------
class ChatCompletionResponseChoice(OpenAIBaseModel):
    """The `ChatCompletionResponseChoice` class represents a choice made during a chat completion response,
       including finish reason, index, message, and log probabilities."""
    # https://platform.openai.com/docs/api-reference/chat/object#chat/object-choices
    finish_reason: Literal['stop', 'length', 'content_filter', 'tool_calls', 'function_call']
    index: int
    message: Optional[ChatMessage]
    logprobs: Optional[ChatCompletionLogProbs] = None


class ChatCompletionResponse(OpenAIBaseModel):
    """The `ChatCompletionResponse` class represents a response object for chat completion with specific
       attributes and fields."""
    # https://platform.openai.com/docs/api-reference/chat/object
    id: str = Field(default_factory=lambda: f"chatcmpl-{random_uuid()}")
    choices: List[ChatCompletionResponseChoice]
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    object: Literal["chat.completion"] = "chat.completion"
    usage: UsageInfo


# --------------------ChatCompletionStreamResponse--------------
class DeltaMessage(OpenAIBaseModel):
    """The `DeltaMessage` class represents a message with role, content, tool calls, and a function call
       (deprecated)."""
    role: Optional[Literal['user', 'assistant', 'system']] = None
    content: Optional[str] = None
    tool_calls: List[ToolCall] = Field(default_factory=list)
    function_call: Optional[FunctionCall] = None  # Deprecated and replaced by tool_calls


class ChatCompletionResponseStreamChoice(OpenAIBaseModel):
    """This class represents a choice made during a chat completion response stream, including information
       such as delta message, log probabilities, finish reason, and index."""
    # https://platform.openai.com/docs/api-reference/chat/streaming#chat/streaming-choices
    delta: DeltaMessage
    logprobs: Optional[ChatCompletionLogProbs] = None
    finish_reason: Optional[Literal['stop', 'length', 'content_filter', 'tool_calls', 'function_call']]
    index: int


class ChatCompletionStreamResponse(OpenAIBaseModel):
    """The `ChatCompletionStreamResponse` class represents a response for streaming chat completion with
       specific attributes and choices."""
    # https://platform.openai.com/docs/api-reference/chat/streaming
    id: str = Field(default_factory=lambda: f"chatcmpl-{random_uuid()}")
    choices: List[ChatCompletionResponseStreamChoice]
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    usage: Optional[UsageInfo] = Field(default=None)
