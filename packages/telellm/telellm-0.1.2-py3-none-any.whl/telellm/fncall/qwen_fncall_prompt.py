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
"""qwen_fncall_prompt"""
import copy
import json


# QwenFnCallPrompt  Qwen2FnCallPrompt

class QwenFnCallPrompt:
    """The `QwenFnCallPrompt` class provides methods for processing messages and responses in a
       conversational prompt setting for interacting with APIs."""
    TOOL_DESC = (
        '{name_for_model}: Call this tool to interact with the {name_for_human} API.'
        ' What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters}'
    )

    REACT_INSTRUCTION = """Answer the following questions as best you can. You have access to the following APIs:

    {tools_text}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tools_name_text}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!"""

    @staticmethod
    def process_messages(messages, **kwargs):
        """
        The function `process_messages` processes a list of messages with optional tools and functions
        provided as keyword arguments.
        """
        tools = kwargs.get('tools', None)
        functions = kwargs.get('functions', None)

        # functions
        if not tools and not functions:
            return messages
        if tools:
            functions = [tool.function for tool in tools]

        messages = copy.deepcopy(messages)
        system = messages.pop(0)

        if functions:
            tools_text = []
            tools_name_text = []
            for func_info in functions:
                name = getattr(func_info, "name", "")
                name_m = getattr(func_info, "name_for_model", name)
                name_h = getattr(func_info, "name_for_human", name)
                desc = getattr(func_info, "description", "")
                desc_m = getattr(func_info, "description_for_model", desc)
                tool = QwenFnCallPrompt.TOOL_DESC.format(
                    name_for_model=name_m,
                    name_for_human=name_h,
                    # Hint: You can add the following format requirements in description:
                    #   "Format the arguments as a JSON object."
                    #   "Enclose the code within triple backticks (`) at the beginning and end of the code."
                    description_for_model=desc_m,
                    parameters=json.dumps(getattr(func_info, "parameters", ""), ensure_ascii=False),
                )
                tools_text.append(tool)
                tools_name_text.append(name_m)
            tools_text = '\n\n'.join(tools_text)
            tools_name_text = ', '.join(tools_name_text)
            instruction = (QwenFnCallPrompt.REACT_INSTRUCTION.format(
                tools_text=tools_text,
                tools_name_text=tools_name_text,
            ).lstrip('\n').rstrip())
        else:
            instruction = ""

        messages_with_fccall = messages
        messages = []
        for m_idx, m in enumerate(messages_with_fccall):
            role, content, func_call = m["role"], m["content"], m.get("function_call", None)
            content = content or ""
            content = content.lstrip('\n').rstrip()
            if role == "function":
                messages[-1]["content"] += f'\nObservation: {content}'
                if m_idx == len(messages_with_fccall) - 1:
                    # add a prefix for text completion
                    messages[-1]["content"] += '\nThought:'
            elif role == "assistant":
                if func_call is None:
                    if functions:
                        content = f'Thought: I now know the final answer.\nFinal Answer: {content}'
                else:
                    f_name, f_args = func_call.name, func_call.arguments
                    if not content.startswith("Thought:"):
                        content = f"Thought: {content}"
                    content = f'{content}\nAction: {f_name}\nAction Input: {f_args}'
                if messages[-1]["role"] == "user":
                    messages.append({"role": role, "content": content})
                else:
                    messages[-1]["content"] += "\n" + content
            else:
                # role == 'user'
                messages.append({"role": role, "content": content.lstrip('\n').rstrip()})

        query = ""
        if messages[-1]["role"] == "user":
            query = messages[-1]["content"]
            messages = messages[:-1]

        for i in range(1, len(messages), 2):
            if messages[i]["role"] == 'user' and messages[i + 1]["role"] == 'assistant':
                if instruction and (i == len(messages) - 2):
                    messages[i]["content"] = f'{instruction}\n\nQuestion: {messages[i]["content"]}'
                    instruction = ''
        if instruction:
            query = f'{instruction}\n\nQuestion: {query}'

        # messages
        return [system] + messages + [{"role": "user", "content": query}]

    @staticmethod
    def process_response(content):
        """
        The function `process_response` extracts function name and arguments from a given content string
        and returns the modified content along with the function calls.
        """
        func_name, func_args = '', ''
        i = content.find('\nAction:')
        j = content.find('\nAction Input:')
        k = content.find('\nObservation:')
        if 0 <= i < j:  # If the text has `Action` and `Action input`,
            if k < j:  # but does not contain `Observation`,
                # then it is likely that `Observation` is omitted by the LLM,
                # because the output text may have discarded the stop word.
                content = content.rstrip() + '\nObservation:'  # Add it back.
            k = content.find('\nObservation:')
            func_name = content[i + len('\nAction:'):j].strip()
            func_args = content[j + len('\nAction Input:'):k].strip()

        # function call
        if func_name:
            content = content[:i]
            t = content.find('Thought: ')
            if t >= 0:
                content = content[t + len('Thought: '):]
            content = content.strip()
            function_calls = [{"name": func_name, "arguments": func_args}]
            return content, function_calls

        # None
        z = content.rfind('\nFinal Answer: ')
        if z >= 0:
            content = content[z + len('\nFinal Answer: '):]
        return content, None


class Qwen2FnCallPrompt:
    """The `Qwen2FnCallPrompt` class provides methods for processing messages related to function calls and
       responses in a structured format."""
    FN_NAME = '✿FUNCTION✿'
    FN_ARGS = '✿ARGS✿'
    FN_RESULT = '✿RESULT✿'
    FN_EXIT = '✿RETURN✿'
    FN_STOP_WORDS = [FN_RESULT, FN_EXIT]

    FN_CALL_TEMPLATE_INFO_ZH = """# 工具

    ## 你拥有如下工具：

    {tool_descs}"""

    FN_CALL_TEMPLATE_INFO_EN = """# Tools

    ## You have access to the following tools:

    {tool_descs}"""

    FN_CALL_TEMPLATE_FMT_ZH = """## 你可以在回复中插入零次、一次或多次以下命令以调用工具：

    %s: 工具名称，必须是[{tool_names}]之一。
    %s: 工具输入
    %s: 工具结果
    %s: 根据工具结果进行回复，需将图片用![](url)渲染出来""" % (
        FN_NAME,
        FN_ARGS,
        FN_RESULT,
        FN_EXIT,
    )

    FN_CALL_TEMPLATE_FMT_EN = """## When you need to call a tool, please insert the following command in your reply, \
    which can be called zero or multiple times according to your needs:

    %s: The tool to use, should be one of [{tool_names}]
    %s: The input of the tool
    %s: Tool results
    %s: Reply based on tool results. Images need to be rendered as ![](url)""" % (
        FN_NAME,
        FN_ARGS,
        FN_RESULT,
        FN_EXIT,
    )

    FN_CALL_TEMPLATE_FMT_PARA_ZH = """## 你可以在回复中插入以下命令以并行调用N个工具：

    %s: 工具1的名称，必须是[{tool_names}]之一
    %s: 工具1的输入
    %s: 工具2的名称
    %s: 工具2的输入
    ...
    %s: 工具N的名称
    %s: 工具N的输入
    %s: 工具1的结果
    %s: 工具2的结果
    ...
    %s: 工具N的结果
    %s: 根据工具结果进行回复，需将图片用![](url)渲染出来""" % (
        FN_NAME,
        FN_ARGS,
        FN_NAME,
        FN_ARGS,
        FN_NAME,
        FN_ARGS,
        FN_RESULT,
        FN_RESULT,
        FN_RESULT,
        FN_EXIT,
    )

    FN_CALL_TEMPLATE_FMT_PARA_EN = """## Insert the following command in your reply when you need \
    to call N tools in parallel:

    %s: The name of tool 1, should be one of [{tool_names}]
    %s: The input of tool 1
    %s: The name of tool 2
    %s: The input of tool 2
    ...
    %s: The name of tool N
    %s: The input of tool N
    %s: The result of tool 1
    %s: The result of tool 2
    ...
    %s: The result of tool N
    %s: Reply based on tool results. Images need to be rendered as ![](url)""" % (
        FN_NAME,
        FN_ARGS,
        FN_NAME,
        FN_ARGS,
        FN_NAME,
        FN_ARGS,
        FN_RESULT,
        FN_RESULT,
        FN_RESULT,
        FN_EXIT,
    )

    FN_CALL_TEMPLATE = {
        'zh': FN_CALL_TEMPLATE_INFO_ZH + '\n\n' + FN_CALL_TEMPLATE_FMT_ZH,
        'en': FN_CALL_TEMPLATE_INFO_EN + '\n\n' + FN_CALL_TEMPLATE_FMT_EN,
        'zh_parallel': FN_CALL_TEMPLATE_INFO_ZH + '\n\n' + FN_CALL_TEMPLATE_FMT_PARA_ZH,
        'en_parallel': FN_CALL_TEMPLATE_INFO_EN + '\n\n' + FN_CALL_TEMPLATE_FMT_PARA_EN,
    }

    @staticmethod
    def get_function_description(function, lang) -> str:
        """
        Text description of function
        """
        tool_desc_template = {
            'zh': '### {name_for_human}\n\n{name_for_model}: {description_for_model} 输入参数：{parameters} {args_format}',
            'en': '### {name_for_human}\n\n{name_for_model}: {description_for_model} Parameters: {parameters} {args_format}'  # noqa: E501
        }
        tool_desc = tool_desc_template[lang]
        name = getattr(function, 'name', '')
        name_for_human = getattr(function, 'name_for_human', name)
        name_for_model = getattr(function, 'name_for_model', name)

        if name_for_model == 'code_interpreter':
            args_format = {
                'zh': '此工具的输入应为Markdown代码块。',
                'en': 'Enclose the code within triple backticks (`) at the beginning and end of the code.',
            }
        else:
            args_format = {
                'zh': '此工具的输入应为JSON对象。',
                'en': 'Format the arguments as a JSON object.',
            }
        args_format = getattr(function, 'args_format', args_format[lang])

        return tool_desc.format(name_for_human=name_for_human,
                                name_for_model=name_for_model,
                                description_for_model=function.description,  # noqa
                                parameters=json.dumps(function.parameters, ensure_ascii=False),  # noqa
                                args_format=args_format).rstrip()

    @staticmethod
    def process_messages(messages, **kwargs):
        """
        The function `process_messages` processes messages based on specified tools, functions, and
        language settings.
        """
        tools = kwargs.get('tools', None)
        functions = kwargs.get('functions', None)
        tool_choice = kwargs.get('tool_choice', "auto")
        function_call = kwargs.get('function_call', "auto")
        parallel_tool_calls = kwargs.get('parallel_tool_calls', False)
        lang = kwargs.get('lang', "zh")

        # functions
        if not tools and not functions:
            return messages
        if tools:
            functions = [tool.function for tool in tools]
        # choice
        choice = function_call if function_call != "auto" else (
            tool_choice.function if hasattr(tool_choice, 'function') else tool_choice
        )

        ori_messages = messages

        # Change function_call responses to plaintext responses:
        messages = []
        for msg in copy.deepcopy(ori_messages):
            role, content = msg["role"], msg["content"]
            if role in ("system", "user"):
                messages.append(msg)
            elif role == "assistant":
                content = (content or "")
                tool_calls = msg.get("tool_calls", None)
                function_call = msg.get("function_call", None)
                if tool_calls:
                    function_calls = [tool_call.function for tool_call in tool_calls]
                elif function_call:
                    function_calls = [function_call]
                else:
                    function_calls = []
                if len(function_calls):
                    func_content = '\n' if messages[-1]["role"] == "assistant" else ''
                    for fn_call in function_calls:
                        f_name = fn_call.name
                        f_args = fn_call.arguments
                        if f_args.startswith('```'):  # if code snippet
                            f_args = '\n' + f_args  # for markdown rendering
                        func_content += f'{Qwen2FnCallPrompt.FN_NAME}: {f_name}'
                        func_content += f'\n{Qwen2FnCallPrompt.FN_ARGS}: {f_args}'
                    content += func_content
                if messages[-1]["role"] == "assistant":
                    messages[-1]["content"] += content
                else:
                    messages.append({"role": role, "content": content})
            elif role == "function":
                # f_result
                if content:
                    f_result = content
                else:
                    f_result = ""
                f_exit = f'\n{Qwen2FnCallPrompt.FN_EXIT}: '
                last_text_content = messages[-1]["content"]
                if last_text_content.endswith(f_exit):
                    messages[-1]["content"] = last_text_content[:-len(f_exit)]
                f_result = f'\n{Qwen2FnCallPrompt.FN_RESULT}: ' + f_result + f_exit
                messages[-1]["content"] += f_result

        # Add a system prompt for function calling:
        tool_desc_template = Qwen2FnCallPrompt.FN_CALL_TEMPLATE[lang + ('_parallel' if parallel_tool_calls else '')]
        tool_descs = '\n\n'.join(Qwen2FnCallPrompt.get_function_description(function, lang) for function in functions)
        tool_names = ','.join(
            getattr(function, "name_for_model", getattr(function, "name", "")) for function in functions)  # noqa: E501
        tool_system = tool_desc_template.format(tool_descs=tool_descs, tool_names=tool_names)
        if messages[0]["role"] == "system":
            messages[0]["content"] += '\n\n' + tool_system
        else:
            messages = [{"role": "system", "content": tool_system}] + messages
        # Remove ': ' for continued generation of function calling,
        # because ': ' may form a single token with its following words:
        if messages[-1]["role"] == "assistant":
            last_msg = messages[-1]["content"].split("\n\n")
            for i in range(len(last_msg) - 1, -1, -1):
                if last_msg[i].endswith(f'{Qwen2FnCallPrompt.FN_EXIT}: '):
                    last_msg[i] = last_msg[i][:-2]
                break

        # Add the function_choice prefix:
        if choice not in ('auto', 'none', 'required'):
            choice = choice.name  # noqa
            if messages[-1]["role"] == "assistant":
                last_msg = messages[-1]
                if last_msg["content"]:
                    if last_msg["content"].endswith(Qwen2FnCallPrompt.FN_EXIT):
                        last_msg["content"] += ': \n'
                    else:
                        last_msg["content"] += '\n'
                messages = messages[:-1]
            else:
                last_msg = {"role": "assistant", "content": ""}
            last_msg["content"] += f'{Qwen2FnCallPrompt.FN_NAME}: {choice}'
            messages = messages + [last_msg]

        return messages

    @staticmethod
    def process_response(content, **kwargs):
        """
        The function `process_response` parses and processes content to extract function calls and
        arguments based on specified parameters.
        """
        tool_choice = kwargs.get('tool_choice', "auto")
        function_call = kwargs.get('function_call', "auto")
        parallel_tool_calls = kwargs.get('parallel_tool_calls', False)

        # choice
        choice = function_call if function_call != "auto" else (
            tool_choice.function if hasattr(tool_choice, 'function') else tool_choice
        )

        # Prepend a prefix for function_choice:
        if choice not in ('auto', 'none', 'required'):
            choice = choice.name  # noqa
            output = content
            if output.lstrip().startswith(Qwen2FnCallPrompt.FN_ARGS):
                # Prepend this prefix only if the model correctly completes it
                output = f'{Qwen2FnCallPrompt.FN_NAME}: {choice}\n' + output
            content = output

        # Convert plaintext responses to function_call responses:
        i = content.find(f'{Qwen2FnCallPrompt.FN_NAME}:')

        # If no function call:
        if i < 0:
            show_text = Qwen2FnCallPrompt.remove_incomplete_special_tokens(content)
            if show_text:
                return show_text, None

        new_content = ""
        function_calls = []
        # If it says something before function call:
        if i > 0:
            answer = content[:i].lstrip('\n').rstrip()
            if answer.endswith('\n'):
                answer = answer[:-1]
            show_text = Qwen2FnCallPrompt.remove_incomplete_special_tokens(answer)
            if show_text:
                new_content = show_text
            content = content[i:]

        # If it has function call:
        for part in content.split(f'{Qwen2FnCallPrompt.FN_NAME}:'):
            if not part:
                continue
            if part.endswith('\n'):
                part = part[:-1]

            arg_sep = f'{Qwen2FnCallPrompt.FN_ARGS}:'
            i = part.find(arg_sep)
            if i < 0:
                fn_name = part.strip()
                list_of_fn_args = ['']
            else:
                fn_name = part[:i].strip()
                list_of_fn_args = [_.strip() for _ in part[i + len(arg_sep):].split(arg_sep)]
            fn_name = Qwen2FnCallPrompt.remove_incomplete_special_tokens(fn_name)
            for fn_args in list_of_fn_args:
                fn_args = Qwen2FnCallPrompt.remove_incomplete_special_tokens(fn_args)
                fn_args = Qwen2FnCallPrompt.remove_trailing_comment_of_fn_args(fn_args)
                function_calls.append({"name": fn_name, "arguments": fn_args})

        # Keep only one function call if parallelism is disabled
        if not parallel_tool_calls:
            if function_calls:
                function_calls = [function_calls[0]]

        return new_content, function_calls

    # Mainly for removing incomplete trailing special tokens when streaming the output
    @staticmethod
    def remove_incomplete_special_tokens(text: str) -> str:
        """Mainly for removing incomplete trailing special tokens when streaming the output"""
        special_tokens = (
            Qwen2FnCallPrompt.FN_NAME, Qwen2FnCallPrompt.FN_ARGS,
            Qwen2FnCallPrompt.FN_RESULT, Qwen2FnCallPrompt.FN_EXIT
        )
        text = text.rstrip()
        if text.endswith(special_tokens):
            for s in special_tokens:
                if text.endswith(s):
                    text = text[:-len(s)]
                    break
        else:
            trail_start = text.rfind('✿')
            trail_token = text[trail_start:]
            for s in special_tokens:
                if s.startswith(trail_token):
                    text = text[:trail_start]
                    break
        text = text.lstrip('\n').rstrip()
        return text

    # For hotfix bad-cases such as `{"arg1": "value1"} <!-- this is an example comment -->`.
    @staticmethod
    def remove_trailing_comment_of_fn_args(fn_args: str):
        """For hotfix bad-cases such as `{"arg1": "value1"} <!-- this is an example comment -->`."""
        fn_args = fn_args.strip()

        if fn_args.startswith('{'):
            k = fn_args.rfind('}')
            if k > 0:
                fn_args = fn_args[:k + 1]

        if fn_args.startswith('```'):
            k = fn_args.rfind('\n```')
            if k > 0:
                fn_args = fn_args[:k + 4]

        return fn_args
