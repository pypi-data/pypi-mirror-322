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
入口函数
"""
import logging
import os
import shutil
import sys

import uvicorn
from dotenv import load_dotenv
from telellm.config.config import CFG
from telellm.utils.logger_utils import get_logger


if os.environ.get("RUNTIME_ENV", "") == "local":
    load_dotenv()

# setup logging format and logger
logger = logging.getLogger()
logger = get_logger(logger=logger, level=CFG.LOG.LOG_LEVEL.upper())


def grace_exit():
    """clean lock path"""
    LOCK_PATH = f'/tmp/{CFG["SERVICE"]["NAME"]}'
    if os.path.exists(LOCK_PATH) and os.path.isdir(LOCK_PATH):
        shutil.rmtree(LOCK_PATH)
        logger.info(f"Exit, clean lock path: {LOCK_PATH}")
        sys.exit(0)


def start_service():
    """
    Starts the FastAPI application server if the framework is FastAPI.
    Logs the server start information and runs the FastAPI app using Uvicorn.
    """
    if CFG.SERVICE.FRAMEWORK.lower() == "fastapi":
        logger.info("Init, start fastapi at %s", CFG.SERVICE.PORT)

        log_config = uvicorn.config.LOGGING_CONFIG  # 定制 fastapi 日志格式

        uvicorn.run(
            "app.servers.fastapi_server:app",
            host=CFG.SERVICE.HOST,
            port=CFG.SERVICE.PORT,
            workers=CFG.SERVICE.PROCESS_NUM,
            log_config=log_config,
        )

    else:
        logger.fatal(f"Init, unsupport framework {CFG.SERVICE.FRAMEWORK}")

    grace_exit()
