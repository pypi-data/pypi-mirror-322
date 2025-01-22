import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

from balto.artifacts.resources.base import GraphResource
from balto.artifacts.resources.types import NodeType
from balto.artifacts.resources.v1.components import DependsOn, RefArgs, CompiledResource
from balto.artifacts.resources.v1.owner import Owner
from dbt_common.contracts.config.base import BaseConfig
from balto.artifacts.resources.v1.config import NodeConfig
from dbt_common.dataclass_schema import StrEnum


@dataclass
class ScheduleConfig(NodeConfig):
    materialized: str = "schedule"
    enabled: bool = True

    @classmethod
    def validate(cls, data):
        super().validate(data)
        if data.get("materialized") and data.get("materialized") != "schedule":
            raise ValidationError("A schedule must have a materialized value of 'schedule'")


@dataclass
class Schedule(CompiledResource):
    resource_type: Literal[NodeType.Schedule]
    config: ScheduleConfig = field(default_factory=ScheduleConfig)
    description: str = ""
    schedule: str = ""
    selector: str = ""
    label: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=lambda: time.time())
