from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from huntflow_api_client.models.response.coworkers import Permission


class UserResponse(BaseModel):
    id: int = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="User name")
    member_type: str = Field(..., alias="type", description="User type (role)")
    head: Optional[int] = Field(None, description="Head user ID")
    email: Optional[EmailStr] = Field(None, description="Email")
    meta: Optional[dict] = Field(None, description="Additional meta information")
    permissions: List[Permission] = Field(default_factory=list, description="User permissions")

    class Config:
        allow_population_by_field_name = True
