# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from pydantic import BaseModel, ConfigDict


class SwarmBaseModel(BaseModel):
    """Base model configuration for Swarm types.

    Enables arbitrary types, docstrings as descriptions, and strict field checking.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_attribute_docstrings=True,
        extra="forbid",
    )
