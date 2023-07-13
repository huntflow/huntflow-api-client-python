from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.consts import ActionLogType


class User(BaseModel):
    id: PositiveInt = Field(..., description="Coworker ID")
    name: str = Field(..., description="Coworker name")
    email: Optional[EmailStr] = Field(None, description="Email")
    phone: Optional[str] = Field(None, description="Phone number")
    meta: Optional[dict] = Field(None, description="Additional information")


class ActionLog(BaseModel):
    id: PositiveInt = Field(..., description="Action log ID")
    user: User = Field(..., description="User who performed the action")
    log_type: ActionLogType = Field(..., description="Action log type")
    created: datetime = Field(..., description="Date and time of creating an action log")
    action: str = Field(..., description="Action")
    ipv4: str = Field(..., description="IP address")
    data: Optional[dict] = Field(None, description="Action data")


class ActionLogsResponse(BaseModel):
    items: List[ActionLog]
    next_id: Optional[PositiveInt] = Field(None, description="The next action log ID")
