from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, PositiveInt

from huntflow_api_client.models.common import Applicant, JsonRequestModel


class ApplicantResumeData(BaseModel):
    body: Optional[str] = Field(None, description="Resume text", example="Resume text for example")


class ApplicantResumeCreate(BaseModel):
    auth_type: Optional[str] = Field(None, description="Auth type", example="NATIVE")
    account_source: Optional[PositiveInt] = Field(None, description="Resume source ID", example=5)
    data: Optional[ApplicantResumeData] = Field(
        None,
        description="Resume data",
        example={"body": "Resume text"},
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        description=("Upload files<br>" "List of file's ID attached to the applicant resume"),
        example=[1, 2, 3],
    )


class ApplicantResumeUpdateData(BaseModel):
    body: Optional[str] = Field(..., description="Resume text", example="Resume text for example")


class ApplicantResumeUpdateRequest(BaseModel):
    account_source: Optional[PositiveInt] = Field(..., description="Resume source ID", example=5)
    data: Optional[ApplicantResumeUpdateData] = Field(
        ...,
        description="Resume data",
        example={"body": "Resume text"},
    )
    files: Optional[List[PositiveInt]] = Field(
        [],
        max_items=1,
        description=("Upload files<br>" "List of file's ID attached to the applicant resume"),
        example=[1],
    )


class ApplicantSocial(BaseModel):
    social_type: Literal["TELEGRAM"] = Field(..., description="Type", example="TELEGRAM")
    value: str = Field(..., description="Value", example="TelegramUsername")


class ApplicantCreateRequest(Applicant, JsonRequestModel):
    birthday: Optional[date] = Field(None, description="Date of birth", example="2000-01-01")
    externals: Optional[List[ApplicantResumeCreate]] = Field(
        None,
        max_items=1,
        description="List of applicant's resumes",
    )
    social: List[ApplicantSocial] = Field(
        [],
        max_items=1,
        description="List of applicant's social accounts",
    )


class ApplicantUpdateRequest(Applicant, JsonRequestModel):
    birthday: Optional[date] = Field(None, description="Date of birth", example="2000-01-01")
    social: Optional[List[ApplicantSocial]] = Field(
        None,
        max_items=1,
        description="List of applicant's social accounts",
    )
