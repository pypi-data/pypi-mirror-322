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

# coding: utf-8
"""
__init__.py
"""
import glob
from importlib import import_module
from os.path import basename, dirname, isfile, join


def init_app(app):
    """
    Initializes the app by dynamically importing and including routers from all Python modules 
    (except for __init__.py) in the current directory.
    """
    modules = glob.glob(join(dirname(__file__), "*.py"))
    modules = [
        basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
    ]
    for m in modules:
        app.include_router(import_module(f".{m}", package=__name__).router)
