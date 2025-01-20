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
提供rest接口通用函数的模块
"""
from telellm.status.http_status import HTTPStatus


def make_response(data=None, status=HTTPStatus.SUCCESS):
    """
    Constructs a standardized response dictionary with a status code, result data, and a message.
    """
    if data is None:
        data = {}

    return {"code": status.value, "result": data, "message": status.message}


def make_exception_response(code, message, details):
    """
    Constructs a standardized exception response dictionary with a code, message, and detailed information.
    """
    return {"code": code, "message": message, "details": details}
