from dataclasses import dataclass
from typing import Literal

from balto.artifacts.resources.types import NodeType
from balto.artifacts.resources.v1.components import CompiledResource


@dataclass
class SqlOperation(CompiledResource):
    resource_type: Literal[NodeType.SqlOperation]
