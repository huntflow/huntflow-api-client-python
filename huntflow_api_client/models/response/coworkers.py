from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from huntflow_api_client.models.common import PaginatedResponse
from huntflow_api_client.models.consts import MemberType


class Permission(BaseModel):
    permission: str = Field(..., description="Permission name")
    value: Optional[str] = Field(None, description="Permission value")
    vacancy: Optional[int] = Field(None, description="Vacancy ID")


class CoworkerResponse(BaseModel):
    id: int = Field(..., description="Coworker ID")
    member: int = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="Coworker name")
    type: MemberType = Field(..., description="Coworker type (role)")
    head: Optional[int] = Field(None, description="Head user ID")
    email: Optional[EmailStr] = Field(None, description="Email")
    meta: Optional[dict] = Field(None, description="Additional meta information")
    permissions: List[Permission] = Field(default_factory=list, description="Coworker permissions")

    model_config = ConfigDict(populate_by_name=True)


class CoworkersListResponse(PaginatedResponse):
    total_items: Optional[int] = Field(..., description="Total number of items")
    items: List[CoworkerResponse] = Field(..., description="List of coworkers")
