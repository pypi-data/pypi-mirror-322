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
Health route
"""
from fastapi import APIRouter
from telellm.config.const import HEALTH_RESPONSE

router = APIRouter(
    tags=["health"],
)


@router.get("/qc")
async def read_status():
    """
    Returns the health status of the system.
    """
    return HEALTH_RESPONSE
