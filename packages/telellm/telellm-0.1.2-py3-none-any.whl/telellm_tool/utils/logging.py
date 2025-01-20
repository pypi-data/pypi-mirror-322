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
"""logging"""
import os
import stat
import logging
from logging.handlers import RotatingFileHandler


class Singleton(type):
    """
    A metaclass that ensures only one instance of a class is created, enforcing the Singleton design pattern.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def change_to_readonly(file_name):
    """
    Changes the file permissions of the specified file to read-only for all users.
    """
    current_permissions = os.stat(file_name).st_mode
    new_permissions = current_permissions & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    os.chmod(file_name, new_permissions)


def create_log_file(log_file):
    """
    Creates a log file with the specified name if it doesn't exist, and sets the file permissions to 640.
    """
    mode = 0o640
    if not os.path.exists(log_file):
        with os.fdopen(os.open(log_file, os.O_CREAT, mode), "w"):
            pass
    os.chmod(log_file, mode)


class CustomRotatingFileHandler(RotatingFileHandler):
    """
    A custom log handler that rotates the log files, changes the permissions of the rotated file to readonly,
    and creates a new log file for logging.
    """
    def rotate(self, source, dest):
        super().rotate(source, dest)
        change_to_readonly(dest)
        create_log_file(source)


# 定义日志封装类
class Logger(metaclass=Singleton):
    """
    A singleton logger class that handles logging to a file and console with rotation and custom permissions.
    The logger supports setting log levels, rotating log files, and ensuring directories exist before logging.
    """
    def __init__(self,
                 log_path='./instance',
                 max_bytes=1024 * 1024,
                 backup_count=1,
                 log_level='DEBUG',
                 logger_name = 'benchmark',
                 open_stream_handler=True):
        self._logger = logging.getLogger(logger_name)
        self.log_file = logger_name + ".log"
        if self._logger.handlers:
            return
        self.log_level = log_level
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        # 根据配置的日志级别设置日志记录器的级别
        self._logger.setLevel(levels.get(self.log_level.upper(), logging.DEBUG))

        # 设置日志格式
        file_logging_format = logging.Formatter(
            '%(asctime)s|%(levelname)s|%(pathname)s:%(funcName)s:%(lineno)s|%(message)s'
        )

        if self.log_level == "INFO":
            file_logging_format = logging.Formatter(
                '%(asctime)s|%(levelname)s|%(funcName)s:%(lineno)s|%(message)s'
            )
        # 创建文件处理器并将日志写入到指定的文件中
        self.make_dirs_if_not_exist(input_dir=log_path)
        create_log_file(os.path.join(log_path, self.log_file))
        file_handler = CustomRotatingFileHandler(os.path.join(log_path, self.log_file), mode='a', maxBytes=max_bytes,
                                           backupCount=backup_count)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(file_logging_format)

        # 添加文件处理器到日志记录器
        self._logger.addHandler(file_handler)

        # 添加控制台输出
        if open_stream_handler:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(file_logging_format)
            self._logger.addHandler(stream_handler)


    @property
    def logger(self):
        """logger"""
        return self._logger

    @staticmethod
    def make_dirs_if_not_exist(input_dir):
        """make_dirs_if_not_exist"""
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
        os.chmod(input_dir, 0o750)

    def set_log_level(self, log_level):
        """set_log_level"""
        self.log_level = log_level
        self._logger.setLevel(log_level)

    def set_log_path(self, log_path):
        """set_log_path"""
        self.make_dirs_if_not_exist(log_path)
        file_handler = CustomRotatingFileHandler(os.path.join(log_path, self.log_file),
                                           mode='a',
                                           maxBytes=1024 * 1024,
                                           backupCount=1)
        # 添加文件处理器到日志记录器
        self._logger.addHandler(file_handler)
        