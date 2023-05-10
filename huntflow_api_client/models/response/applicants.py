from datetime import date, datetime
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.common import Applicant, PaginatedResponse
from huntflow_api_client.models.consts import AgreementState


class ApplicantTag(BaseModel):
    tag: int = Field(..., description="Tag ID", example=1)
    id: int = Field(..., description="Applicant's tag ID", example=1)


class ApplicantLink(BaseModel):
    id: Optional[int] = Field(None, description="Link ID", example=7)
    status: int = Field(..., description="Vacancy status ID", example=12)
    updated: datetime = Field(
        ...,
        description="The date of the applicant's update at a vacancy",
    )
    changed: datetime = Field(
        ...,
        description="The date of the latest changes at the current recruitment stage",
    )
    vacancy_id: int = Field(..., alias="vacancy", description="Vacancy ID", example=4)

    class Config:
        allow_population_by_field_name = True


class ApplicantResume(BaseModel):
    id: int = Field(..., description="Resume ID", example=1)
    auth_type: Optional[str] = Field(None, description="The format of resume", example="HH")
    account_source: Optional[int] = Field(None, description="Resume source ID", example=10)
    updated: Optional[datetime] = Field(
        None,
        description="The date and time of resume update",
    )


class ApplicantAgreement(BaseModel):
    state: Optional[AgreementState] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
        example=AgreementState.accepted,
    )
    decision_date: Optional[datetime] = Field(
        None,
        description="Date of applicant's decision to personal data processing",
    )


class ApplicantDouble(BaseModel):
    double: int = Field(..., description="The ID of a duplicated applicant", example=8)


class ApplicantSocial(BaseModel):
    id: PositiveInt = Field(..., description="Social ID", example=1)
    social_type: str = Field(..., description="Type", example="TELEGRAM")
    value: str = Field(..., description="Value", example="TelegramUsername")
    verified: bool = Field(..., description="Verification flag")
    verification_date: Optional[datetime] = Field(None, description="Verification date")


class ApplicantItem(Applicant):
    id: int = Field(..., description="Applicant ID", example=1)
    account: int = Field(..., description="Organization ID", example=5)
    photo_url: Optional[str] = Field(
        None,
        description="A link to an applicant’s photo",
        example="https://hh.resume/12341234",
    )
    birthday: Optional[date] = Field(None, description="Date of birth", example="2020-01-01")
    created: Optional[datetime] = Field(
        ...,
        description="Date and time of adding an applicant",
    )
    email: Optional[Union[EmailStr, str]] = Field(
        None,
        description="Email address",
        example="mail@mail.ru",  # type: ignore
    )
    tags: List[ApplicantTag] = Field(..., description="List of tags")
    links: List[ApplicantLink] = Field(..., description="Applicant's vacancies")
    external: Optional[List[ApplicantResume]] = Field(None, description="Applicant's resume")
    agreement: Optional[ApplicantAgreement] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
        example=AgreementState.declined,
    )
    doubles: list[ApplicantDouble] = Field(..., description="List of duplicates")
    social: list[ApplicantSocial] = Field(..., description="List of applicant's social accounts")


class ApplicantListResponse(PaginatedResponse):
    total_items: Optional[int] = Field(..., description="Total number of items", example=50)
    items: List[ApplicantItem] = Field(..., description="List of applicants")


class ApplicantCreateResponse(Applicant):
    id: int = Field(..., description="Applicant ID", example=19)
    created: datetime = Field(
        ...,
        description="Date and time of adding an applicant",
    )
    birthday: Optional[date] = Field(None, description="Date of birth", example="2020-01-01")
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="Upload files<br>The list of file's ID attached to the applicant",
        example=[1, 2, 3],
    )
    doubles: List[ApplicantDouble] = Field(..., description="List of duplicates")
    agreement: Optional[ApplicantAgreement] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
        example=AgreementState.sent,
    )
    external: List[ApplicantResume] = Field(..., description="Applicant's resume")
    social: List[ApplicantSocial] = Field(..., description="List of applicant's social accounts")
