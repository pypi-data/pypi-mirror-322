from typing import List

# preserving import path during dbt/artifacts refactor
from balto.artifacts.resources.types import (  # noqa
    AccessType,
    ModelLanguage,
    NodeType,
    RunHookType,
)

EXECUTABLE_NODE_TYPES: List["NodeType"] = [
    NodeType.Model,
    NodeType.Test,
    NodeType.Snapshot,
    NodeType.Analysis,
    NodeType.Operation,
    NodeType.Seed,
    NodeType.Schedule,
    NodeType.Documentation,
    NodeType.RPCCall,
    NodeType.SqlOperation,
]

REFABLE_NODE_TYPES: List["NodeType"] = [
    NodeType.Model,
    NodeType.Seed,
    NodeType.Snapshot,
]

VERSIONED_NODE_TYPES: List["NodeType"] = [
    NodeType.Model,
]
