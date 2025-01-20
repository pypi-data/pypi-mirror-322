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
HTTP/REST server
"""
import base64
import logging
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from telellm.utils.rest_utils import make_exception_response
from telellm.config.config import CFG
from telellm.routers import init_app
from telellm.utils.fastapi_utils import lifespan
from telellm.status.http_status import HTTPStatus
from telellm.status.status_exception import StatusException

logger = logging.getLogger(__name__)


class BasicAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that handles basic authentication for HTTP requests.
    It checks the 'Authorization' header and validates the provided credentials.
    """
    def __init__(self, _app, username: str, password: str):
        super().__init__(_app)
        self.required_credentials = base64.b64encode(
            f'{username}:{password}'.encode()).decode()

    async def dispatch(self, request: Request, call_next):
        authorization: str = request.headers.get('Authorization')
        if authorization:
            try:
                _, credentials = authorization.split()
                if credentials == self.required_credentials:
                    return await call_next(request)
            except ValueError:
                pass

        headers = {'WWW-Authenticate': 'Basic'}
        return Response(status_code=401, headers=headers)


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_app(app)

if CFG.LLM.AUTH:
    app.add_middleware(BasicAuthMiddleware,
                       username=CFG.LLM.AUTH.split(':')[0],
                       password=CFG.LLM.AUTH.split(':')[1])


@app.exception_handler(StatusException)
def handle_status_exception(req: Request, exc: StatusException):
    """
    Handles StatusException by logging the error and returning a structured JSON response.
    """
    reqid = (
        req.headers["x-request-id"] if "x-request-id" in req.headers else uuid4().hex
    )
    logger.info("Reqid: %s, catch a StatusException, code=%s", reqid, exc.code)
    data = make_exception_response(
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )
    return JSONResponse(content=data, status_code=400)


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(req: Request, exc: StarletteHTTPException):
    """
    Handles HTTP exceptions by logging the error and returning a structured JSON response 
    based on the exception status code.
    """
    reqid = (
        req.headers["x-request-id"] if "x-request-id" in req.headers else uuid4().hex
    )
    logger.info("Reqid: %s, catch a StarletteHTTPException, code=%s", reqid, exc.status_code)
    if exc.status_code == 405:
        # 400002 请求方法错误
        data = make_exception_response(
            code=HTTPStatus.REQUEST_METHOD_ERR.value,
            message=HTTPStatus.REQUEST_METHOD_ERR.message,
            details=HTTPStatus.REQUEST_METHOD_ERR.details,
        )
        return JSONResponse(content=data, status_code=405)
    if exc.status_code == 404:
        # 400001 请求路径错误
        data = make_exception_response(
            code=int(HTTPStatus.REQUEST_PATH_ERR.value),
            message=HTTPStatus.REQUEST_PATH_ERR.message,
            details=HTTPStatus.REQUEST_PATH_ERR.details,
        )
        return JSONResponse(content=data, status_code=404)
    # 400001 请求路径错误
    data = make_exception_response(
        code=exc.status_code,
        message=exc.detail,
        details=exc.detail,
    )
    return JSONResponse(content=data, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(req: Request, exc: RequestValidationError):
    """
    Handles request validation errors by logging the error and returning a structured JSON response 
    based on the type of validation issue encountered in the request body.
    """
    reqid = (
        req.headers["x-request-id"] if "x-request-id" in req.headers else uuid4().hex
    )
    logger.info("Reqid: %s, catch a RequestValidationError, msg: %s", reqid, exc)
    if not exc.body:
        # 400003 请求体内容为空
        data = make_exception_response(
            code=HTTPStatus.BODY_EMPTY_ERR.value,
            message=HTTPStatus.BODY_EMPTY_ERR.message,
            details=HTTPStatus.BODY_EMPTY_ERR.details,
        )
        return JSONResponse(content=data, status_code=400)
    if isinstance(exc.body, str):
        if "=" in exc.body:
            # 400004 请求体非 json 格式
            data = make_exception_response(
                code=HTTPStatus.BODY_JSON_ERR.value,
                message=HTTPStatus.BODY_JSON_ERR.message,
                details=HTTPStatus.BODY_JSON_ERR.details,
            )
            return JSONResponse(content=data, status_code=400)
        # 400005 请求体类型错误
        data = make_exception_response(
            code=HTTPStatus.BODY_TYPE_ERR.value,
            message=HTTPStatus.BODY_TYPE_ERR.message,
            details=HTTPStatus.BODY_TYPE_ERR.details,
        )
        return JSONResponse(content=data, status_code=400)
    if not isinstance(exc.body, dict):
        content_type = req.headers.get("content-type", None)
        if "multipart/form-data" in content_type:
            # 400004 请求体非 data 格式
            data = make_exception_response(
                HTTPStatus.BODY_DATA_ERR.value,
                HTTPStatus.BODY_DATA_ERR.message,
                HTTPStatus.BODY_DATA_ERR.details,
            )
            return JSONResponse(content=data, status_code=400)
        if content_type != "application/json":
            # 400004 请求体非 json 格式
            data = make_exception_response(
                HTTPStatus.BODY_JSON_ERR.value,
                HTTPStatus.BODY_JSON_ERR.message,
                HTTPStatus.BODY_JSON_ERR.details,
            )
            return JSONResponse(content=data, status_code=400)
        # 400005 请求体类型错误
        data = make_exception_response(
            code=HTTPStatus.BODY_TYPE_ERR.value,
            message=HTTPStatus.BODY_TYPE_ERR.message,
            details=HTTPStatus.BODY_TYPE_ERR.details,
        )
        return JSONResponse(content=data, status_code=400)
    if exc.errors():
        error = exc.errors()[0]
        error_msg = error.get('msg', None)
        error_type = error.get('type', None)

        if error_msg and error_msg == "Field required":
            # 400006 必须的参数未传
            field = error.get('loc')[1]
            data = make_exception_response(
                code=HTTPStatus.CUSTOMIZE_MUST_PRAM_ERR.value,
                message=HTTPStatus.CUSTOMIZE_MUST_PRAM_ERR.message,
                details=HTTPStatus.CUSTOMIZE_MUST_PRAM_ERR.details.format(custom_field=field),
            )
            logger.info("reqid: %s, %s must param err.", reqid, field)
        elif error_msg and "Input should be a valid" in error_msg:
            # 400008 请求体的字段类型错误
            field = error.get('loc')[1]
            data = make_exception_response(
                code=HTTPStatus.CUSTOMIZE_TYPE_ERR.value,
                message=HTTPStatus.CUSTOMIZE_TYPE_ERR.message,
                details=HTTPStatus.CUSTOMIZE_TYPE_ERR.details.format(custom_field=field),
            )
            logger.info("reqid: %s, %s type err.", reqid, field)
        elif error_type and error_type == "literal_error" and error_msg and "Input should be" in error_msg:
            # 400010 请求体的参数字段值设置错误
            field = error.get('loc')[1]
            input0 = error.get('input')
            data = make_exception_response(
                code=HTTPStatus.VALUE_ERR.value,
                message=HTTPStatus.VALUE_ERR.message,
                details=f"{field} 字段值不符合规范，输入 {input0} 不正确",
            )
            logger.info("reqid: %s, %s value err, input: %s is incorrect.", reqid, field, input0)
        else:
            # 400005 请求体类型错误
            data = make_exception_response(
                code=HTTPStatus.BODY_TYPE_ERR.value,
                message=HTTPStatus.BODY_TYPE_ERR.message,
                details=HTTPStatus.BODY_TYPE_ERR.details,
            )
        return JSONResponse(content=data, status_code=400)


@app.exception_handler(Exception)
def handle_exception(req: Request, exc: Exception):
    """
    Handles general exceptions by logging the error and returning a structured JSON response
    indicating a server error.
    """
    reqid = (
        req.headers["x-request-id"] if "x-request-id" in req.headers else uuid4().hex
    )
    logger.info("Reqid: %s, catch a Exception, msg: %s", reqid, exc)
    # 500001 服务接口异常，请联系管理员
    data = make_exception_response(
        code=HTTPStatus.SERVER_ERR.value,
        message=HTTPStatus.SERVER_ERR.message,
        details=HTTPStatus.SERVER_ERR.details,
    )
    return JSONResponse(content=data, status_code=500)
