from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from huntflow_api_client.models.common import ForeignUser, PaginatedResponse
from huntflow_api_client.models.consts import UserControlTaskAction, UserControlTaskStatus


class ForeignUserResponse(ForeignUser):
    pass


class ForeignUsersListResponse(PaginatedResponse):
    items: List[ForeignUserResponse] = Field(
        default_factory=List,
        description="Users with foreign identifiers",
    )


class CreatedUserControlTaskResponse(BaseModel):
    task_id: UUID = Field(..., description="Task ID")
    action: UserControlTaskAction = Field(..., description="Task action")
    created: datetime = Field(..., description="Task creation time")


class UserControlTaskResponse(BaseModel):
    id: UUID = Field(..., description="Task ID")
    account_id: int = Field(..., description="Organization account ID")
    action: UserControlTaskAction = Field(..., description="Task action")
    status: UserControlTaskStatus = Field(..., description="Task status")
    data: Optional[Dict] = Field(None, description="Task result")
    comment: Optional[str] = Field(None, description="Comment (in case of error)")
    created: datetime = Field(..., description="Task creation time")
    completed: Optional[datetime] = Field(None, description="Task completion time")


class UserInternalIDResponse(BaseModel):
    id: int = Field(..., description="User ID")
