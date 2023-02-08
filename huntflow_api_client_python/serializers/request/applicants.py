import typing as t
from datetime import date

from pydantic import BaseModel, Field, PositiveInt

from huntflow_api_client_python.serializers.common import Applicant


class ApplicantResumeData(BaseModel):
    body: str = Field(None, description="Resume text", example="Resume text for example")


class ApplicantResumeCreate(BaseModel):
    auth_type: str = Field(None, description="Auth type", example="NATIVE")
    account_source: PositiveInt = Field(
        None, description="Resume source ID", example=5
    )
    data: t.Optional[ApplicantResumeData] = Field(
        None, description="Resume data", example={"body": "Resume text"}
    )
    files: t.Optional[t.List[PositiveInt]] = Field(
        None,
        description="List of file's ID attached to the applicant resume",
        example=[1, 2, 3],
    )


class ApplicantSocial(BaseModel):
    social_type: str = Field(..., description="Type", example="TELEGRAM")
    value: str = Field(..., description="Value", example="TelegramUsername")


class ApplicantCreateRequest(Applicant):
    birthday: date = Field(None, description="Date of birth", example="2000-01-01")
    externals: t.List[ApplicantResumeCreate] = Field(
        None, max_items=1, description="List of applicant's resumes"
    )
    social: t.List[ApplicantSocial] = Field(
        [], max_items=1, description="List of applicant's social accounts",
    )


class ApplicantUpdateRequest(Applicant):
    birthday: date = Field(None, description="Date of birth", example="2000-01-01")
    social: t.List[ApplicantSocial] = Field(
        None, max_items=1, description="List of applicant's social accounts",
    )


class ApplicantVacancySplitRequest(BaseModel):
    applicant: int = Field(..., description="Applicant ID", example=123)
    status: int = Field(..., description="Account vacancy status ID", example=21)
    fill_quota: t.Optional[int] = Field(None, description="Fill quota ID for hiring", example=321)
    employment_date: t.Optional[date] = Field(
        None, description="Employment date", example="2021-12-31"
    )
    rejection_reason: t.Optional[int] = Field(
        None, description="Rejection reason ID for trash status", example=456
    )
