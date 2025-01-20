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
"""status_exception"""
class StatusException(Exception):
    """
    Custom exception that represents an error with a specific status code, message, and details.
    It allows for optional custom fields and details to be included in the exception.
    """
    def __init__(self, status, custom_field=None, custom_details=None):
        self.code = status.value
        self.message = status.message
        self.details = status.details
        if custom_field:
            self.details = status.details.format(custom_field=custom_field)
        if custom_details:
            self.details = custom_details

    def __str__(self):
        return f'code: {self.code}, message: {self.message}, details: {self.details}'
