import datetime as dt
import typing as t
from uuid import UUID

from pydantic import BaseModel, Field

from huntflow_api_client.models.consts import TaskState


class TaskLog(BaseModel):
    state: TaskState = Field(..., description="Task status")
    timestamp: float = Field(..., description="Unix timestamp of the task state change")
    datetime_: dt.datetime = Field(
        ...,
        description="Date and time of the task state change (ISO 8601)",
        alias="datetime",
    )
    comment: t.Optional[str] = Field(None, description="Comment text")


class DelayedTaskResponse(BaseModel):
    task_id: UUID = Field(..., description="Task ID")
    state: TaskState = Field(..., description="Current task status")
    created: float = Field(
        ...,
        description="Unix timestamp of task creation",
    )
    updated: t.Optional[float] = Field(
        None,
        description="Unix timestamp of the last task update",
    )
    created_datetime: dt.datetime = Field(
        ...,
        description="Date and time of task creation (ISO 8601)",
    )
    updated_datetime: t.Optional[dt.datetime] = Field(
        None,
        description="Date and time of the last task update (ISO 8601)",
    )
    states_log: t.List[TaskLog] = Field(..., description="Task change log")
