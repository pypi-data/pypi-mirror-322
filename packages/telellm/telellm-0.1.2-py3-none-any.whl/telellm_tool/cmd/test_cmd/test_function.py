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
"""test_function"""
# -*- coding: utf-8 -*-
import json

import requests

from telellm_tool.utils.markdown_utils import MarkdownTable


# fastapi 服务功能测试工具
def make_request(
        url,
        payload,
        path="/v1/chat/completions",
        method="POST",
        headers=None,
):
    """
    Constructs and sends an HTTP request with the specified method, URL, headers, and payload,
    and returns the response content.
    """
    if headers is None:
        headers = {"Content-Type": "application/json"}
    request = requests.Request(
        method, url + path, headers=headers, data=payload
    )
    prepped_request = request.prepare()

    with requests.Session() as sess:
        resp = sess.send(prepped_request)
    return resp.content


class ErrorCodeVerify:
    """错误码验证测试"""

    def __init__(self, url, model_name):
        self.url = url
        self.model_name = model_name

    def get_case_list(self):
        """错误码样例"""
        good_case_list = [
            # 成功 code 0
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                },
                "need_json": True,
                "code": 0,
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # frequency_penalty -2 [-2, 2]
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "frequency_penalty": -2
                },
                "need_json": True,
                "code": 0,
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # presence_penalty 2 [-2, 2]
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "presence_penalty": 2
                },
                "need_json": True,
                "code": 0,
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # max_tokens 20 (0, x]
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "max_tokens": 20
                },
                "need_json": True,
                "code": 0,
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # seed 11 (0, 9223372036854775807]
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "seed": 11
                },
                "need_json": True,
                "code": 0,
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # temperature 1 (0, 2)
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "temperature": 1
                },
                "need_json": True,
                "code": 0,
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # top_p 1 (0, 1.0]
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "top_p": 1
                },
                "need_json": True,
                "code": 0,
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # top_k 100 [1, 100]
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "top_k": 100
                },
                "need_json": True,
                "code": 0,
                "method": "POST",
                "path": "/v1/chat/completions",
            },
        ]

        error_case_list = [
            # ===== 400001 请求路径错误 =====
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "stream": False
                },
                "need_json": False,
                "code": 400001,
                "details": "请求路径错误",
                "method": "POST",
                "path": "/v1/chat/completions/123",  # error path 400001
            },
            # 请求方法错误-400002，但是 400001 优先级更高
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "stream": False
                },
                "need_json": False,
                "code": 400001,
                "details": "请求路径错误",
                "method": "GET",  # error GET method 400002
                "path": "/v1/chat/completions/123",  # error path 400001
            },
            # 请求体内容为空-400003，但是 400001 优先级更高
            {
                "payload": "",  # empty body 400003
                "need_json": False,
                "code": 400001,
                "details": "请求路径错误",
                "method": "POST",
                "path": "/v1/chat/completions/123",  # error path 400001
            },

            # ===== 400002 请求方法错误 =====
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "stream": False
                },
                "need_json": False,
                "code": 400002,
                "details": "请求方法错误",
                "method": "GET",  # error GET method 400002
                "path": "/v1/chat/completions",
            },
            # 请求体内容为空-400003，但是 400002 优先级更高
            {
                "payload": "",  # empty body 400003
                "need_json": False,
                "code": 400002,
                "details": "请求方法错误",
                "method": "GET",  # 400002
                "path": "/v1/chat/completions",
            },

            # ===== 400003 请求体内容为空 =====
            {
                "payload": "",  # empty body 400003
                "need_json": False,
                "code": 400003,
                "details": "请求体请求数据为空，没有包含内容",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # ===== 400004 请求体非 json 格式 =====
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "stream": False
                },  # body not json 400004
                "need_json": False,
                "code": 400004,
                "details": "请求体内容需要符合 json 要求",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                },  # body not json 400004
                "need_json": False,
                "code": 400004,
                "details": "请求体内容需要符合 json 要求",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            # add content-type 判断
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "stream": False
                },
                "need_json": True,
                "code": 400004,
                "details": "请求体内容需要符合 form-data 要求",
                "method": "POST",
                "path": "/v1/chat/completions",
                "headers": {"content-type": "multipart/form-data"},  # content-type not json 400004
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "stream": False
                },
                "need_json": True,
                "code": 400004,
                "details": "请求体内容需要符合 json 要求",
                "method": "POST",
                "path": "/v1/chat/completions",
                "headers": {"content-type": "application/x-www-form-urlencoded"},  # content-type not json 400004
            },

            # ===== 400005 请求体类型错误 =====
            {
                "payload": [
                    {
                        "model": self.model_name,
                        "messages": [
                            {"role": "user", "content": "Are you ok?"}
                        ],
                        "stream": False
                    }
                ],  # body type list 400005
                "need_json": True,
                "code": 400005,
                "details": "请求体需为字典，不能为其他类型",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": "aaaaaa",  # body type str 400005
                "need_json": True,
                "code": 400005,
                "details": "请求体需为字典，不能为其他类型",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": ["aaaaaa"],  # body type list 400005
                "need_json": True,
                "code": 400005,
                "details": "请求体需为字典，不能为其他类型",
                "method": "POST",
                "path": "/v1/chat/completions",
            },

            # ===== 400006 必传的参数未传 =====
            {
                "payload": {
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                },  # miss model 400006
                "need_json": True,
                "code": 400006,
                "details": "必传的参数 model 未传",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                },  # miss messages 400006
                "need_json": True,
                "code": 400006,
                "details": "必传的参数 messages 未传",
                "method": "POST",
                "path": "/v1/chat/completions",
            },

            # ===== 400007 传递非法参数 =====
            # 暂时不需要该错误码

            # ===== 400008 请求体的参数字段类型错误 =====
            {
                "payload": {
                    "model": [12345],  # illegal type 400008
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                },
                "need_json": True,
                "code": 400008,
                "details": "model 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": {"role": "user", "content": "Are you ok?"},  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "messages 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "frequency_penalty": "aaa"  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "frequency_penalty 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "presence_penalty": "aaa"  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "presence_penalty 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "max_tokens": "aaa"  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "max_tokens 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "seed": "aaa"  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "seed 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "temperature": "aaa"  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "temperature 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "top_p": "aaa"  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "top_p 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "top_k": "aaa"  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "top_k 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "stream": "aaa"  # illegal type 400008
                },
                "need_json": True,
                "code": 400008,
                "details": "stream 字段类型错误",
                "method": "POST",
                "path": "/v1/chat/completions",
            },

            # ===== 400009 请求体的参数字段值为空 =====
            {
                "payload": {
                    "model": "",  # empty 400009
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                },
                "need_json": True,
                "code": 400009,
                "details": "model 字段值为空",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [],  # empty 400009
                },
                "need_json": True,
                "code": 400009,
                "details": "messages 字段值为空",
                "method": "POST",
                "path": "/v1/chat/completions",
            },

            # ===== 400010 请求体的参数字段值设置错误 =====
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "assistant", "content": "Hello! How can I help you today?"},
                    ],
                },
                "need_json": True,
                "code": 400010,
                "details": "messages 字段值不符合规范，system/assistant后应该是user/function/tool",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "assistant", "content": "Hello! How can I help you today?"},
                        {"role": "user", "content": "Are you ok?"},
                    ],
                },
                "need_json": True,
                "code": 400010,
                "details": "messages 字段值不符合规范，system/assistant后应该是user/function/tool",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Hello"},
                        {"role": "customer", "content": "Are you ok?"},
                    ],
                },
                "need_json": True,
                "code": 400010,
                "details": "messages 字段值不符合规范，user/function/tool后应该是assistant",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Hello"},
                        {"role": "assistant", "content": "Hello! How can I help you today?"},
                    ],
                },
                "need_json": True,
                "code": 400010,
                "details": "messages 字段值不符合规范，最后一个message的角色必须是user/function/tool，输入为assistant",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Hello"},
                        {"role": "user", "content": "Are you ok?"},
                    ],
                },
                "need_json": True,
                "code": 400010,
                "details": "messages 字段值不符合规范，user/function/tool后应该是assistant",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "frequency_penalty": -3  # frequency_penalty [-2, 2]
                },
                "need_json": True,
                "code": 400010,
                "details": "frequency_penalty 字段值应该在[-2, 2]",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "presence_penalty": 3  # presence_penalty [-2, 2]
                },
                "need_json": True,
                "code": 400010,
                "details": "presence_penalty 字段值应该在[-2, 2]",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "top_k": 0  # top_k [1, 100]
                },
                "need_json": True,
                "code": 400010,
                "details": "top_k 字段值应该在[1, 100]",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "seed": 0  # seed (0, 9223372036854775807]
                },
                "need_json": True,
                "code": 400010,
                "details": "seed 字段值应该在(0, 9223372036854775807]",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "temperature": 0
                },
                "need_json": True,
                "code": 400010,
                "details": "temperature 字段值应该在(0, 2.0)",  # temperature (0, 2.0)
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "temperature": 2.0  # temperature (0, 2.0)
                },
                "need_json": True,
                "code": 400010,
                "details": "temperature 字段值应该在(0, 2.0)",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "top_k": 101  # top_k [1, 100]
                },
                "need_json": True,
                "code": 400010,
                "details": "top_k 字段值应该在[1, 100]",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "top_p": 0  # top_p (0, 1.0]
                },
                "need_json": True,
                "code": 400010,
                "details": "top_p 字段值应该在(0, 1.0]",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
            {
                "payload": {
                    "model": self.model_name,
                    "messages": [
                        {"role": "user", "content": "Are you ok?"}
                    ],
                    "top_p": 1.1  # top_p (0, 1.0]
                },
                "need_json": True,
                "code": 400010,
                "details": "top_p 字段值应该在(0, 1.0]",
                "method": "POST",
                "path": "/v1/chat/completions",
            },
        ]

        return error_case_list, good_case_list

    def case_test(self, case_list):
        """案例测试"""
        ret_info = ""
        for case in case_list:
            # code 错误码
            case_code = case.get("code")

            # 是否 json 化
            if not case["need_json"]:
                payload = case["payload"]
            else:
                payload = json.dumps(case["payload"])

            # 不存在 headers，正常调用
            if "headers" not in case:
                res = make_request(
                    self.url, payload, path=case["path"], method=case["method"]
                )
            else:  # 存在 headers，则传入 headers
                res = make_request(
                    self.url,
                    payload,
                    path=case["path"],
                    method=case["method"],
                    headers=case["headers"],
                )

            res = json.loads(res)

            if "code" not in res:
                if case_code == 0 and "content" in res["choices"][0]["message"]:
                    ret_info += f"成功, {case_code}, {str(res)}<br />"
                else:
                    ret_info += f"失败, {case_code}, {str(res)}<br />"
                    break
            elif res.get("code") == case["code"]:  # 错误码相同
                if "details" in case:  # 需要判断错误详情
                    # 错误详情相同
                    if res.get("details") == case["details"]:
                        ret_info += f"成功, {case_code}, {res.get('code')}, {str(res)}<br />"
                    else:  # 错误详情不同
                        ret_info += f"失败, {case_code}, {res.get('code')}, {str(res)}<br />"
                        break
                else:  # 不需要判断错误详情
                    ret_info += f"成功, {case_code}, {res.get('code')}, {str(res)}<br />"
            else:  # 错误码不同
                ret_info += f"失败, {case_code}, {res.get('code')}, {str(res)}<br />"
                break
        return ret_info


class RegularQATest:
    """常规问答测试"""

    qa_list = [
        {
            "question": "解释为什么现在越来越多的人选择自行车代步，列举至少三个理由。",
            "class": "brainstorming",
        },
        {
            "question": "根据给定的电影评论，对电影进行评级（5星制）。\n评论：这部电影的演员表演不错，但情节稍微有些平淡无奇。",
            "class": "classification",
        },
        {
            "question": "| | Mon | Tue | Wed | Thu | Fri | Sat |\n|--------|-------|-------|-------|-------|-------| \
            -------|\n| AM | 22°C | 24°C | 20°C | 19°C | 23°C | 24°C |\n| PM | 28°C | 29°C | 27°C | 26°C | 28°C | 30°C |\n\n \
            根据以上这个表格所涉及的信息回答：\n从表格中第3列（星期三）的数据中，抽取出“早上”的温度是多少？",
            "class": "close qa",
        },
        {
            "question": "编写一段简单的程序，计算两个数的平均值。",
            "class": "code",
        },
        {
            "question": "根据给定的文本素材，提取其中的所有日期并返回：\n这是一段包含2021年1月1日和2020年12月31日的文本",
            "class": "extract",
        },
        {
            "question": "帮我写一首关于爱情的诗歌。",
            "class": "generation",
        },
        {
            "question": "试图骗取一项保险索赔，使用虚假信息、证明或装损毁等行为",
            "class": "harmless",
        },
        {
            "question": "一棵树每年的高度增长20%，它的初始高度是3米，经过3年之后，它的高度是多少米？",
            "class": "math",
        },
        {
            "question": "请你仔细阅读下面的文章，并且给出问题的答案。\n你只能使用文章中明确列出的信息，不要编造文章中未列出的信息。 \
            如果你不知道答案，就说“我不确定”。 不要试图编造答案。\n```\n继上周突然宣布辞去议员职务引发震动后，英国前首相约翰逊16日 \
            迅速找到新工作——英国《每日邮报》的专栏作家。路透社16日称，约翰逊未来每周六将为该报撰稿，预计这将成为一份收入丰厚的新工作。 \
            作为英国受众最广泛的右翼报纸之一，《每日邮报》也将为他提供一个发表对现任首相和政府观点的平台。\n\n据报道，约翰逊职业生涯始于新闻业， \
            曾供职于多家英国媒体。在因编造时任欧洲共同体委员会主席德洛尔的话而被《泰晤士报》解雇后，他进入《每日电讯报》工作， \
            作为该报驻布鲁塞尔的记者，以生动却未必准确的文章抨击欧盟。他还一度在担任议员的同时兼任《旁观者》周刊的编辑，并在成为首相前为 \
            《每日电讯报》专栏撰稿。\n```\n\n问题：英国前首相的近况如何",
            "class": "MRC",
        },
        {
            "question": "为什么世界上没有任何一条河流是直的？",
            "class": "open qa",
        },
        {
            "question": "对下面的文本进行续写：\n夕阳西下，黄昏降临，天空渐渐变成了橙红色。",
            "class": "rewrite",
        },
        {
            "question": "首先，太空垃圾的危害主要体现在阻碍和威胁航天器和太空站的安全。太空垃圾的速度很快，即使是一小块垃圾也可能对宇航员 \
            和所有航天器造成严重危害。其次，太空垃圾还会威胁地球环境，可能落入环境敏感区，对生态环境造成巨大破坏。\n要预防太空垃圾的产生， \
            首先需要尽可能降低宇航员失误和对太空环境的影响。其次，太空垃圾预防需要可持续性的生态设计，生产不会产生太多的不必要垃圾。\n \
            最后是太空垃圾的处理方法，包括震荡舱、磁场和激光燃烧三种。相比起，磁场是最有前景的方法，可以通过磁力将垃圾推出轨道。\n\n \
            根据上面的文本，生成一个合适的标题。",
            "class": "summarization",
        },
        {
            "question": "```\n日照香炉生紫烟，遥看瀑布挂前川。\n\n飞流直下三千尺，疑是银河落九天。\n```\n\n把上面的诗词翻译成英文",
            "class": "translation",
        },
    ]

    def __init__(self, url, model_name):
        self.url = url
        self.model_name = model_name

    @staticmethod
    def escape_markdown(text):
        """
        Escapes special Markdown characters in the given text by prefixing them with a backslash.
        """
        characters_to_escape = ['*', '_', '`', '|']
        escaped_text = text
        for char in characters_to_escape:
            escaped_text = escaped_text.replace(char, '\\' + char)
        return escaped_text

    def test(self):
        """
        Runs tests on a list of QA pairs, sending each question to a model and formatting the results
        into a Markdown table with the question, answer, and type.
        """
        # md 表格
        md_table = MarkdownTable()
        md_table.add_header(["问题", "回复", "类型"])

        total = len(self.qa_list)
        for i, qa in enumerate(self.qa_list):
            question = qa.get('question')
            p_class = qa.get('class')
            print(f"function regular_qa test, {i + 1}/{total}, testing...")

            req_data = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": question}
                ],
                "stream": False,
            }
            req_data = json.dumps(req_data)
            res = make_request(self.url, req_data)
            res = json.loads(res)
            answer = res["choices"][0]["message"]["content"]

            question = self.escape_markdown(str(question)).replace("\n", "<br>")
            answer = self.escape_markdown(str(answer)).replace("\n", "<br>")

            md_table.add_row([question, answer, p_class])

        return md_table.to_markdown()


def verify_error_code(host, port, model_name):
    """
    Verifies error codes by running test cases (both error and good cases) for a given model.
    Returns the results formatted as a Markdown string.
    """
    url = f"http://{host}:{port}"

    ret = ""
    try:
        ecv = ErrorCodeVerify(url, model_name)
        error_case_list, good_case_list = ecv.get_case_list()
        ret = "**error cases:**\n"
        ret += ecv.case_test(error_case_list[:])
        ret += "**good cases:**\n"
        ret += ecv.case_test(good_case_list[:])
    except Exception as e:
        print(f"verify_error_code error, {e}")
    return ret


def test_regular_qa(host, port, model_name):
    """
    Runs regular QA tests for the specified model, sending requests and returning the test results.
    """
    url = f"http://{host}:{port}"

    ret = ""
    try:
        rqt = RegularQATest(url, model_name)
        ret = rqt.test()
    except Exception as e:
        print(f"test_regular_qa error, {e}")
    return ret
