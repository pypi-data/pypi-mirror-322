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
"""base_fncall_prompt"""
from telellm.config.config import CFG
from telellm.fncall.glm_fncall_prompt import GLM4FnCallPrompt
from telellm.fncall.qwen_fncall_prompt import Qwen2FnCallPrompt, QwenFnCallPrompt


class BaseFnCallPrompt:
    """This class `BaseFnCallPrompt` is used to determine the type of function call prompt based on a
       configuration setting and provides methods to process messages and responses accordingly."""
    def __init__(self):
        # QwenFnCallPrompt  Qwen2FnCallPrompt GLM4FnCallPrompt
        fncall_type = CFG.LLM.FNCALL_TYPE

        if fncall_type == "qwen":
            self.base = QwenFnCallPrompt
        elif fncall_type == "qwen2":
            self.base = Qwen2FnCallPrompt
        elif fncall_type == "glm4":
            self.base = GLM4FnCallPrompt
        else:
            raise ValueError("FNCALL_TYPE设置错误, 请检查！")

    def process_messages(self, messages, tools=None, functions=None,
                         tool_choice="auto", function_call="auto",
                         parallel_tool_calls=False, lang="zh"):
        """
        The `process_messages` function processes messages using specified tools and functions with
        optional parameters for tool choice, function call, parallel tool calls, and language.
        """
        kwargs = {
            "tools": tools, "functions": functions,
            "tool_choice": tool_choice, "function_call": function_call,
            "parallel_tool_calls": parallel_tool_calls, "lang": lang
        }
        return self.base.process_messages(messages, **kwargs)

    def process_response(self, content,
                         tools=None, functions=None, tool_choice="auto", function_call="auto",
                         parallel_tool_calls=False):
        """
        The function `process_response` takes in content and optional parameters, then calls another
        method `process_response` with the provided arguments.
        """
        kwargs = {
            "tools": tools, "functions": functions,
            "tool_choice": tool_choice, "function_call": function_call, "parallel_tool_calls": parallel_tool_calls
        }
        return self.base.process_response(content, **kwargs)
