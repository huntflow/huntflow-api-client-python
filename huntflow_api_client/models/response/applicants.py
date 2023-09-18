from datetime import date, datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PositiveInt

from huntflow_api_client.models.common import Applicant, PaginatedResponse
from huntflow_api_client.models.consts import AgreementState as AgreementStateEnum


class ApplicantTag(BaseModel):
    tag: int = Field(..., description="Tag ID")
    id: int = Field(..., description="Applicant's tag ID")


class ApplicantLink(BaseModel):
    id: Optional[int] = Field(None, description="Link ID")
    status: int = Field(..., description="Vacancy status ID")
    updated: datetime = Field(
        ...,
        description="The date of the applicant's update at a vacancy",
    )
    changed: datetime = Field(
        ...,
        description="The date of the latest changes at the current recruitment stage",
    )
    vacancy_id: int = Field(..., alias="vacancy", description="Vacancy ID")

    model_config = ConfigDict(populate_by_name=True)


class ApplicantResume(BaseModel):
    id: int = Field(..., description="Resume ID")
    auth_type: Optional[str] = Field(None, description="The format of resume")
    account_source: Optional[int] = Field(None, description="Resume source ID")
    updated: Optional[datetime] = Field(
        None,
        description="The date and time of resume update",
    )


class ApplicantAgreement(BaseModel):
    state: Optional[AgreementStateEnum] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
    )
    decision_date: Optional[datetime] = Field(
        None,
        description="Date of applicant's decision to personal data processing",
    )


class ApplicantDouble(BaseModel):
    double: int = Field(..., description="The ID of a duplicated applicant")


class ApplicantSocial(BaseModel):
    id: PositiveInt = Field(..., description="Social ID")
    social_type: str = Field(..., description="Type")
    value: str = Field(..., description="Value")
    verified: bool = Field(..., description="Verification flag")
    verification_date: Optional[datetime] = Field(None, description="Verification date")


class ApplicantItem(Applicant):
    id: int = Field(..., description="Applicant ID")
    account: int = Field(..., description="Organization ID")
    photo_url: Optional[str] = Field(
        None,
        description="A link to an applicant’s photo",
    )
    birthday: Optional[date] = Field(None, description="Date of birth")
    created: Optional[datetime] = Field(
        None,
        description="Date and time of adding an applicant",
    )
    email: Union[EmailStr, str, None] = Field(
        None,
        description="Email address",
    )
    tags: List[ApplicantTag] = Field(..., description="List of tags")
    links: List[ApplicantLink] = Field(..., description="Applicant's vacancies")
    external: Optional[List[ApplicantResume]] = Field(None, description="Applicant's resume")
    agreement: Optional[ApplicantAgreement] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
    )
    doubles: List[ApplicantDouble] = Field(..., description="List of duplicates")
    social: List[ApplicantSocial] = Field(..., description="List of applicant's social accounts")


class ApplicantListResponse(PaginatedResponse):
    total_items: Optional[int] = Field(..., description="Total number of items")
    items: List[ApplicantItem] = Field(..., description="List of applicants")


class ApplicantCreateResponse(Applicant):
    id: int = Field(..., description="Applicant ID")
    created: datetime = Field(
        ...,
        description="Date and time of adding an applicant",
    )
    birthday: Optional[date] = Field(None, description="Date of birth")
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="Upload files<br>The list of file's ID attached to the applicant",
    )
    doubles: List[ApplicantDouble] = Field(..., description="List of duplicates")
    agreement: Optional[ApplicantAgreement] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
    )
    external: List[ApplicantResume] = Field(..., description="Applicant's resume")
    social: List[ApplicantSocial] = Field(..., description="List of applicant's social accounts")


class ApplicantSearchItem(BaseModel):
    id: int = Field(..., description="Applicant ID")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    middle_name: Optional[str] = Field(None, description="Middle name")
    birthday: Optional[date] = Field(None, description="Date of birth")
    phone: Optional[str] = Field(None, description="Phone number")
    skype: Optional[str] = Field(None, description="Skype login")
    email: Union[EmailStr, str, None] = Field(None, description="Email address")
    money: Optional[str] = Field(None, description="Salary expectation")
    position: Optional[str] = Field(None, description="Candidate’s occupation")
    company: Optional[str] = Field(None, description="Candidate’s place of work")
    photo: Optional[int] = Field(None, description="Candidate’s photo ID")
    photo_url: Optional[str] = Field(None, description="A link to a candidate’s photo")
    created: datetime = Field(..., description="Date and time of adding a candidate")


class ApplicantSearchByCursorResponse(BaseModel):
    items: List[ApplicantSearchItem] = Field(..., description="List of applicants")
    next_page_cursor: Optional[str] = Field(None, description="Next page cursor")
