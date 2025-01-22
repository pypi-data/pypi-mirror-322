import random
from typing import Optional, Type

from balto.artifacts.schemas.results import NodeStatus, RunStatus
from balto.contracts.graph.manifest import Manifest
from balto.events.types import LogScheduleResult, LogStartLine
from balto.graph import ResourceTypeSelector
from balto.node_types import NodeType
from balto.task.base import BaseRunner
from dbt_common.events.base_types import EventLevel
from dbt_common.events.functions import fire_event
from dbt_common.events.types import Formatting
from dbt_common.exceptions import DbtInternalError

from .printer import print_run_end_messages
from .run import ModelRunner, RunTask


class ScheduleRunner(ModelRunner):
    def describe_node(self) -> str:
        return "schedule {}".format(self.get_node_representation())

    def before_execute(self) -> None:
        fire_event(
            LogStartLine(
                description=self.describe_node(),
                index=self.node_index,
                total=self.num_nodes,
                node_info=self.node.node_info,
            )
        )

    def compile(self, manifest: Manifest):
        return self.node

    def print_result_line(self, result):
        model = result.node
        level = EventLevel.ERROR if result.status == NodeStatus.Error else EventLevel.INFO
        fire_event(
            LogScheduleResult(
                status=result.status,
                result_message=result.message,
                index=self.node_index,
                total=self.num_nodes,
                execution_time=result.execution_time,
                schema=self.node.schema,
                relation=model.alias,
                node_info=model.node_info,
            ),
            level=level,
        )


class ScheduleTask(RunTask):
    def raise_on_first_error(self) -> bool:
        return False

    def get_node_selector(self):
        if self.manifest is None or self.graph is None:
            raise DbtInternalError("manifest and graph must be set to perform node selection")
        return ResourceTypeSelector(
            graph=self.graph,
            manifest=self.manifest,
            previous_state=self.previous_state,
            resource_types=[NodeType.Schedule],
        )

    def get_runner_type(self, _) -> Optional[Type[BaseRunner]]:
        return ScheduleRunner

    def task_end_messages(self, results) -> None:
        print_run_end_messages(results)
