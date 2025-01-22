from dataclasses import dataclass
from typing import Literal, Optional

from balto.artifacts.resources.types import NodeType
from balto.artifacts.resources.v1.components import CompiledResource


@dataclass
class HookNode(CompiledResource):
    resource_type: Literal[NodeType.Operation]
    index: Optional[int] = None
