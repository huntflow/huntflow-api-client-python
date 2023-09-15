from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from huntflow_api_client.models.consts import MemberType
from huntflow_api_client.models.response.coworkers import Permission


class UserResponse(BaseModel):
    id: int = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="User name")
    type: MemberType = Field(..., description="User type (role)")
    head: Optional[int] = Field(None, description="Head user ID")
    email: Optional[EmailStr] = Field(None, description="Email")
    meta: Optional[dict] = Field(None, description="Additional meta information")
    permissions: List[Permission] = Field(default_factory=list, description="User permissions")

    model_config = ConfigDict(populate_by_name=True)
