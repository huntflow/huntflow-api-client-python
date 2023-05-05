from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.consts import MemberType


class MeResponse(BaseModel):
    id: PositiveInt = Field(..., description="User ID", example=10)
    name: Optional[str] = Field(None, description="User name", example="John Doe")
    position: Optional[str] = Field(None, description="User occupation", example="Head")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number", example="89999999999")
    locale: str = Field(..., description="User locale", example="ru_RU")


class Organization(BaseModel):
    id: PositiveInt = Field(..., description="Organization ID", example=10)
    name: str = Field(..., description="Organization name", example="Huntflow")
    nick: str = Field(..., description="Short organization name", example="huntflow")
    member_type: MemberType = Field(
        ...,
        description="Role of the current user in the organization",
        example=MemberType.owner,
    )
    production_calendar: Optional[PositiveInt] = Field(
        None,
        description="Production calendar ID",
        example=1,
    )


class OrganizationsListResponse(BaseModel):
    items: List[Organization] = Field(..., description="List of available organizations")


class OrganizationInfoResponse(BaseModel):
    id: PositiveInt = Field(..., description="Organization ID", example=10)
    name: str = Field(..., description="Organization name", example="Huntflow")
    nick: str = Field(..., description="Short organization name", example="huntflow")
    locale: str = Field(..., description="Organization locale", example="ru_RU")
    photo: Optional[AnyHttpUrl] = Field(
        None,
        description="Organization logo url",
        example="https://huntflow.dev/logo.jpg",
    )
