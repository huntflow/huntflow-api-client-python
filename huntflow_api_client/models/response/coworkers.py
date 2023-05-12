from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from huntflow_api_client.models.common import PaginatedResponse


class Permission(BaseModel):
    permission: str = Field(..., description="Permission name")
    value: Optional[str] = Field(None, description="Permission value")
    vacancy: Optional[int] = Field(None, description="Vacancy ID")


class CoworkerResponse(BaseModel):
    id: int = Field(..., description="Coworker ID")
    member: int = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="Coworker name")
    member_type: str = Field(..., alias="type", description="Coworker type (role)")
    head: Optional[int] = Field(None, description="Head user ID")
    email: Optional[EmailStr] = Field(None, description="Email")
    meta: Optional[dict] = Field(None, description="Additional meta information")
    permissions: List[Permission] = Field(default_factory=list, description="Coworker permissions")

    class Config:
        allow_population_by_field_name = True


class CoworkersListResponse(PaginatedResponse):
    total_items: Optional[int] = Field(..., description="Total number of items")
    items: List[CoworkerResponse] = Field(..., description="List of coworkers")
