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
"""logger_utils"""
import os
import sys
import time
import logging
from threading import Thread
from logging.handlers import TimedRotatingFileHandler

ALLOW_LOG_LEVEL = ['FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
DYNAMIC_THREAD = False


def get_logger(logger=None, name='tele', level='info', log_path=None, backup_count=7, terminal=True,
               dynamic_level=False, dynamic_interval=30):
    """
    Creates and configures a logger with options for log level, file output, terminal output,
    and dynamic log level adjustment.
    """
    # 默认仅提供级别：FATAL, ERROR, WARNING, INFO, DEBUG
    logging.addLevelName(logging.DEBUG, 'DEBUG')
    logging.addLevelName(logging.INFO, 'INFO ')
    logging.addLevelName(logging.WARNING, 'WARN ')
    logging.addLevelName(logging.ERROR, 'ERROR')
    logging.addLevelName(logging.FATAL, 'FATAL')

    if logger:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
        logger.propagate = True
    else:
        logger = logging.getLogger(name)

    logging.Formatter.default_msec_format = '%s.%03d'
    # 24小时制
    logging.Formatter.default_time_format = '%Y%m%dT%H:%M:%S'
    log_formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s:%(lineno)s %(threadName)s - %(message)s')
    if log_path is not None:
        handler = TimedRotatingFileHandler(log_path, when='midnight', interval=1, backupCount=backup_count)
        handler.suffix = '%Y-%m-%d'
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)

    if terminal:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)
    log_level = level.upper().strip()
    if log_level not in ALLOW_LOG_LEVEL:
        logger.warning('Init: LOG_LEVEL %s is not allowed, set to default INFO', log_level)
        log_level = "INFO"
    logger.setLevel(log_level)
    global DYNAMIC_THREAD
    if dynamic_level and not DYNAMIC_THREAD:
        DYNAMIC_THREAD = True
        dynamic_level_thread = Thread(target=dynamic_change_log_level, args=(logger, log_level, dynamic_interval),
                                      name='LogThread', daemon=True)
        dynamic_level_thread.start()

    return logger


def dynamic_change_log_level(logger, log_level, dynamic_interval):
    """
    Monitors the environment variable 'LOG_LEVEL' and dynamically adjusts the log level of the logger
    based on changes, with a specified interval for checking.
    """
    current_log_level = log_level
    logger.info('Init: Start dynamic log level thread succeed')
    while True:
        log_level = os.environ.get('LOG_LEVEL', None)
        if log_level is not None:
            log_level = log_level.upper().strip()
            if log_level in ALLOW_LOG_LEVEL and log_level != current_log_level:
                logger.setLevel(log_level)
                if log_level == 'ERROR':
                    logger.error(f'Timer: Change LOG_LEVEL from {current_log_level} to {log_level}')
                if log_level == 'WARNING':
                    logger.warning(f'Timer: Change LOG_LEVEL from {current_log_level} to {log_level}')
                else:
                    logger.info(f'Timer: Change LOG_LEVEL from {current_log_level} to {log_level}')
        time.sleep(dynamic_interval)
