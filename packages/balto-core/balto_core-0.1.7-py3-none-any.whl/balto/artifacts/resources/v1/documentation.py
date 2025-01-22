from dataclasses import dataclass
from typing import Literal

from balto.artifacts.resources.base import BaseResource
from balto.artifacts.resources.types import NodeType


@dataclass
class Documentation(BaseResource):
    resource_type: Literal[NodeType.Documentation]
    block_contents: str
