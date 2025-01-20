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
"""model"""
import time
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class OpenAIBaseModel(BaseModel):
    """The `OpenAIBaseModel` class allows extra fields on a case-by-case basis with the specified model
       configuration."""
    # forbid: OpenAI API does not allow extra fields
    # allow: Extra fields are allowed on a case-by-case basis
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)


# --------------------ModelCard/ModelList--------------
class ModelCard(OpenAIBaseModel):
    """The `ModelCard` class defines attributes for a model card with default values and optional fields."""
    # https://platform.openai.com/docs/api-reference/models/object
    id: str
    object: str = 'model'
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = 'owner'
    root: Optional[str] = None
    parent: Optional[str] = None
    max_model_len: Optional[int] = None
    permission: Optional[list] = None


class ModelList(OpenAIBaseModel):
    """The `ModelList` class represents a list of `ModelCard` objects."""
    object: str = 'list'
    data: List[ModelCard] = Field(default_factory=list)
