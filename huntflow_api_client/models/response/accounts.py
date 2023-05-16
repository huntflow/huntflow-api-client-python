from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.consts import MemberType


class MeResponse(BaseModel):
    id: PositiveInt = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="User name")
    position: Optional[str] = Field(None, description="User occupation")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    locale: str = Field(..., description="User locale")


class Organization(BaseModel):
    id: PositiveInt = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    nick: str = Field(..., description="Short organization name")
    member_type: MemberType = Field(
        ...,
        description="Role of the current user in the organization",
    )
    production_calendar: Optional[PositiveInt] = Field(
        None,
        description="Production calendar ID",
    )


class OrganizationsListResponse(BaseModel):
    items: List[Organization] = Field(..., description="List of available organizations")


class OrganizationInfoResponse(BaseModel):
    id: PositiveInt = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    nick: str = Field(..., description="Short organization name")
    locale: str = Field(..., description="Organization locale")
    photo: Optional[AnyHttpUrl] = Field(
        None,
        description="Organization logo url",
    )
