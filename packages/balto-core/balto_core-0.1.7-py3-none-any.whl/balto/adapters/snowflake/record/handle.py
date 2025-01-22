from typing import Any, Optional

from balto.adapters.contracts.connection import Connection
from balto.adapters.record import RecordReplayHandle
from balto.adapters.record.cursor.description import CursorGetDescriptionRecord
from balto.adapters.record.cursor.execute import CursorExecuteRecord
from balto.adapters.record.cursor.fetchone import CursorFetchOneRecord
from balto.adapters.record.cursor.fetchmany import CursorFetchManyRecord
from balto.adapters.record.cursor.fetchall import CursorFetchAllRecord
from balto.adapters.record.cursor.rowcount import CursorGetRowCountRecord
from balto.adapters.snowflake.record.cursor.cursor import SnowflakeRecordReplayCursor
from snowflake.connector.cursor import ResultMetadata


class SnowflakeRecordReplayHandle(RecordReplayHandle):
    """A custom extension of RecordReplayHandle that returns a
    snowflake-connector-specific SnowflakeRecordReplayCursor object."""

    def cursor(self):
        cursor = None if self.native_handle is None else self.native_handle.cursor()
        return SnowflakeRecordReplayCursor(cursor, self.connection)

class DummyReplayHandle():
    """A custom extension of RecordReplayHandle that returns a
    snowflake-connector-specific SnowflakeRecordReplayCursor object."""

    def cursor(self):
        return DummyReplayCursor()


class DummyReplayCursor:

    def __init__(self):
        self.dummy_result = []

    def execute(self, operation, parameters=None) -> None:
        pass

    def fetchone(self) -> Any:
        return self.dummy_result

    def fetchmany(self, size: int) -> Any:
        return self.dummy_result

    def fetchall(self) -> Any:
        return self.dummy_result

    def connection_name(self) -> Optional[str]:
        return "fake_connection"

    @property
    def rowcount(self) -> int:
        return 0

    @property
    def description(self):
        return [
            ResultMetadata(name='created_on', type_code=6, display_size=None, internal_size=None, precision=0, scale=3, is_nullable=True),
            ResultMetadata(name='name', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='database_name', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='schema_name', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='kind', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='comment', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='cluster_by', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='rows', type_code=0, display_size=None, internal_size=None, precision=38, scale=0, is_nullable=True),
            ResultMetadata(name='bytes', type_code=0, display_size=None, internal_size=None, precision=38, scale=0, is_nullable=True),
            ResultMetadata(name='owner', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='retention_time', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='owner_role_type', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='budget', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True),
            ResultMetadata(name='is_dynamic', type_code=2, display_size=None, internal_size=16777216, precision=None, scale=None, is_nullable=True)
        ]

    @property
    def sfqid(self):
        return "sfqid"

    @property
    def sqlstate(self):
        return None
