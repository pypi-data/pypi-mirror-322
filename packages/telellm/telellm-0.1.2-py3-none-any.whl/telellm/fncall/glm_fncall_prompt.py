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
"""glm_fncall_prompt"""
import json
import re
from typing import Union


class GLM4FnCallPrompt:
    """The `GLM4FnCallPrompt` class in Python provides methods for processing messages and responses
       related to tools and function calls."""
    @staticmethod
    def format_tools_choice(tools, functions, tool_choice: Union[str, object], function_call):
        """
        The function `format_tools_choice` formats a list of tools and determines a choice based on
        input parameters.
        """
        if tools:
            new_tools = []
            for tool in tools:
                function = tool.function
                new_tools.append({"type": "function", "function": {
                    "name": function.name, "description": function.description, "parameters": function.parameters
                }})
            tools = new_tools
        else:
            tools = [
                {"type": "function", "function": {
                    "name": function.name, "description": function.description, "parameters": function.parameters
                }} for function in functions
            ]

        # choice
        choice = function_call if function_call != "auto" else (
            tool_choice.function if hasattr(tool_choice, 'function') else tool_choice
        )
        return tools, choice

    @staticmethod
    def process_messages(messages, **kwargs):
        """
        The `process_messages` function processes a list of messages based on specified tools and
        functions, generating new messages with different roles and content.
        """
        tools = kwargs.get('tools', None)
        functions = kwargs.get('functions', None)
        tool_choice = kwargs.get('tool_choice', "auto")
        function_call = kwargs.get('function_call', "auto")

        if not tools and not functions:
            return messages
        # tools and choice
        tools, choice = GLM4FnCallPrompt.format_tools_choice(tools, functions, tool_choice, function_call)

        _messages = messages
        processed_messages = []
        msg_has_sys = False

        def filter_tools(_choice, _tools):
            function_name = _choice.name
            if not function_name:
                return []
            filtered_tools = [
                _tool for _tool in _tools
                if _tool.get('function', {}).get('name') == function_name
            ]
            return filtered_tools

        if choice != "none":
            if hasattr(choice, 'name'):
                tools = filter_tools(choice, tools)
            if tools:
                processed_messages.append(
                    {
                        "role": "system",
                        "content": None,
                        "tools": tools
                    }
                )
                msg_has_sys = True

        if hasattr(choice, 'name') and tools:
            processed_messages.append(
                {
                    "role": "assistant",
                    "metadata": choice.name,
                    "content": ""
                }
            )

        for m in _messages:
            role, content, func_call = m["role"], m["content"], m.get("function_call", None)
            tool_calls = m.get("tool_calls", None)

            if role == "function":
                processed_messages.append(
                    {
                        "role": "observation",
                        "content": content
                    }
                )
            elif role == "tool":
                processed_messages.append(
                    {
                        "role": "observation",
                        "content": content,
                        "function_call": True
                    }
                )
            elif role == "assistant":
                if tool_calls:
                    for tool_call in tool_calls:
                        processed_messages.append(
                            {
                                "role": "assistant",
                                "metadata": tool_call.function.name,
                                "content": tool_call.function.arguments
                            }
                        )
                elif func_call:
                    processed_messages.append(
                        {
                            "role": "assistant",
                            "metadata": func_call.name,
                            "content": func_call.arguments
                        }
                    )
                else:
                    for response in content.split("\n"):
                        if "\n" in response:
                            metadata, sub_content = response.split("\n", maxsplit=1)
                        else:
                            metadata, sub_content = "", response
                        processed_messages.append(
                            {
                                "role": role,
                                "metadata": metadata,
                                "content": sub_content.strip()
                            }
                        )
            else:
                if role == "system" and msg_has_sys:
                    msg_has_sys = False
                    continue
                processed_messages.append({"role": role, "content": content})

        return processed_messages

    @staticmethod
    def process_response(content, **kwargs):
        """
        The function `process_response` processes content based on specified tools and functions,
        extracting function calls and arguments from the content.
        """
        tools = kwargs.get('tools', None)
        functions = kwargs.get('functions', None)
        tool_choice = kwargs.get('tool_choice', "auto")
        function_call = kwargs.get('function_call', "auto")

        if not tools and not functions:
            return content
        # tools and choice
        tools, choice = GLM4FnCallPrompt.format_tools_choice(tools, functions, tool_choice, function_call)

        lines = content.strip().split("\n")
        arguments_json = None
        special_tools = ["cogview", "simple_browser"]
        tools = {tool['function']['name'] for tool in tools} if tools else {}
        use_tool = choice != "none"

        if len(lines) >= 2 and lines[1].startswith("{"):
            line0 = lines[0].strip()

            def get_function_name(_line, _tools):
                for _tool in _tools:
                    if _tool in _line:
                        return _tool
                return None

            is_tool_call = False
            function_name = get_function_name(line0, tools)
            special_function_name = get_function_name(line0, special_tools)
            arguments = "\n".join(lines[1:]).strip()
            if function_name:
                try:
                    arguments_json = json.loads(arguments)
                    is_tool_call = True
                except json.JSONDecodeError:
                    pass
            if special_function_name:
                function_name = special_function_name
                is_tool_call = True

            if is_tool_call and use_tool:
                pos = line0.find(function_name)
                if pos != -1 and pos > 0:
                    content = content[0:pos]
                else:
                    content = ""
                fn_call = {
                    "name": function_name,
                    "arguments": json.dumps(arguments_json if isinstance(arguments_json, dict) else arguments,
                                            ensure_ascii=False)
                }
                if function_name == "simple_browser":
                    search_pattern = re.compile(r'search\("(.+?)"\s*,\s*recency_days\s*=\s*(\d+)\)')
                    match = search_pattern.match(arguments)
                    if match:
                        fn_call["arguments"] = json.dumps({
                            "query": match.group(1),
                            "recency_days": int(match.group(2))
                        }, ensure_ascii=False)
                elif function_name == "cogview":
                    fn_call["arguments"] = json.dumps({
                        "prompt": arguments
                    }, ensure_ascii=False)

                return content.strip(), [fn_call]
        return content.strip(), None
