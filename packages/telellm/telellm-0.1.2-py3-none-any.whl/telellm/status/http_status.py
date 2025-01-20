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
提供http请求状态码的模块
"""
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class HTTPStatus(Enum):
    """HTTP status codes and reason phrases
    Status codes from the following RFCs are all observed:
        * RFC 7231: Hypertext Transfer Protocol (HTTP/1.1), obsoletes 2616
        * RFC 6585: Additional HTTP Status Codes
        * RFC 3229: Delta encoding in HTTP
        * RFC 4918: HTTP Extensions for WebDAV, obsoletes 2518
        * RFC 5842: Binding Extensions to WebDAV
        * RFC 7238: Permanent Redirect
        * RFC 2295: Transparent Content Negotiation in HTTP
        * RFC 2774: An HTTP Extension Framework
    """

    def __new__(cls, value, message, details=''):
        obj = object.__new__(cls)
        obj._value_ = obj

        obj.code = value
        obj.message = message
        obj.details = details
        return obj

    def value(self):
        return self.code

    # success
    SUCCESS = (0, 'success', 'Success')


    ### 通用 40xxxxx ###

    # 400001 请求路径错误
    REQUEST_PATH_ERR = (400001, '请求路径错误', '请求路径错误')

    # 400002 请求方法错误
    REQUEST_METHOD_ERR = (400002, "请求方法错误", "请求方法错误")
    REQUEST_METHOD_POST_ERR = (400002, "请求方法错误", "请求方法错误，请使用 POST 请求")
    REQUEST_METHOD_GET_ERR = (400002, "请求方法错误", "请求方法错误，请使用 GET 请求")

    # 400003 请求体内容为空
    BODY_EMPTY_ERR = (400003, "请求体内容为空", "请求体请求数据为空，没有包含内容")

    # 400004 请求体内容格式不符合
    BODY_JSON_ERR = (400004, "请求体非 json 格式", "请求体内容需要符合 json 要求")
    BODY_DATA_ERR = (400004, "请求体非 form-data 格式", "请求体内容需要符合 form-data 要求")

    # 400005 请求体类型错误
    BODY_TYPE_ERR = (400005, "请求体类型错误", "请求体需为字典，不能为其他类型")

    # 400006 必传的参数未传
    MUST_PRAM_ERR = (400006, "请求参数不完整", "必须的参数未传")
    CUSTOMIZE_MUST_PRAM_ERR = (400006, "请求参数不完整", "必传的参数 {custom_field} 未传")

    # 400008 请求体的字段类型错误
    TYPE_ERR = (400008, "请求体的字段类型错误", "请求体的字段类型错误")
    CUSTOMIZE_TYPE_ERR = (400008, "请求体的字段类型错误", "{custom_field} 字段类型错误")
    CUSTOMIZE_STRING_TYPE_ERR = (400008, "请求体的字段类型错误", "{custom_field} 字段应该是 string 类型")
    CUSTOMIZE_LIST_TYPE_ERR = (400008, "请求体的字段类型错误", "{custom_field} 字段应该是 list 类型")
    CUSTOMIZE_INT_TYPE_ERR = (400008, "请求体的字段类型错误", "{custom_field} 字段应该是 int 类型")
    CUSTOMIZE_BOOL_TYPE_ERR = (400008, "请求体的字段类型错误", "{custom_field} 字段应该是 bool 类型")
    CUSTOMIZE_FLOAT_TYPE_ERR = (400008, "请求体的字段类型错误", "{custom_field} 字段应该是 float 类型")

    # 400009 请求体的参数字段值为空
    EMPTY_ERR = (400009, "请求体的参数字段值为空", "请求体的字段值为空")
    CUSTOMIZE_EMPTY_ERR = (400009, "请求体的参数字段值为空", "{custom_field} 字段值为空")

    # 400010 请求体的参数字段值设置错误
    VALUE_ERR = (400010, "请求体的字段值设置错误", "请求体的字段值不符合规范")

    # 4000015 文件下载错误
    IMAGE_URL_DOWNLOAD_ERR = (400015, "文件下载错误", "图片链接下载错误")


    ### 服务 5xxxxxx ###

    # 500001 server服务错误
    SERVER_ERR = (500001, "服务接口异常，请联系管理员", "服务接口异常，需要联系管理员处理")

    # 500002 模型推理错误
    SERVER_INFER_ERR = (500002, "模型推理异常，请联系管理员", "模型推理异常，需要联系管理员处理")

    # 500003 依赖服务异常
    SERVER_DEPENDENT_ERR = (500003, "依赖服务异常，请联系管理员", "依赖服务异常，请联系管理员")
