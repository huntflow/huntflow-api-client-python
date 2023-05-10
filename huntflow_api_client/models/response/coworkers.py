from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from huntflow_api_client.models.common import PaginatedResponse


class Permission(BaseModel):
    permission: str = Field(..., description="Permission name", example="status")
    value: Optional[str] = Field(None, description="Permission value", example="97")
    vacancy: Optional[int] = Field(None, description="Vacancy ID", example=1)


class CoworkerResponse(BaseModel):
    id: int = Field(..., description="Coworker ID", example=12)
    member: int = Field(..., description="User ID", example=1)
    name: Optional[str] = Field(None, description="Coworker name", example="John Doe")
    member_type: str = Field(
        ...,
        alias="type",
        description="Coworker type (role)",
        example="owner",
    )
    head: Optional[int] = Field(None, description="Head user ID", example=2)
    email: Optional[EmailStr] = Field(None, description="Email", example="mail@gmail.com")
    meta: Optional[dict] = Field(None, description="Additional meta information")
    permissions: List[Permission] = Field(default_factory=list, description="Coworker permissions")

    class Config:
        allow_population_by_field_name = True


class CoworkersListResponse(PaginatedResponse):
    total_items: Optional[int] = Field(..., description="Total number of items", example=50)
    items: List[CoworkerResponse] = Field(..., description="List of coworkers")
