from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, PositiveInt

from huntflow_api_client.models.common import Applicant, JsonRequestModel


class ApplicantResumeData(BaseModel):
    body: Optional[str] = Field(None, description="Resume text")


class ApplicantResumeCreate(BaseModel):
    auth_type: Optional[str] = Field(None, description="Auth type")
    account_source: Optional[PositiveInt] = Field(None, description="Resume source ID")
    data: Optional[ApplicantResumeData] = Field(None, description="Resume data")
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="Upload files<br>" "List of file's ID attached to the applicant resume",
    )


class ApplicantResumeUpdateData(BaseModel):
    body: Optional[str] = Field(..., description="Resume text")


class ApplicantResumeUpdateRequest(BaseModel):
    account_source: Optional[PositiveInt] = Field(..., description="Resume source ID")
    data: Optional[ApplicantResumeUpdateData] = Field(
        ...,
        description="Resume data",
    )
    files: Optional[List[PositiveInt]] = Field(
        [],
        max_items=1,
        description="Upload files<br>" "List of file's ID attached to the applicant resume",
    )


class ApplicantSocial(BaseModel):
    social_type: Literal["TELEGRAM"] = Field(..., description="Type")
    value: str = Field(..., description="Value")


class ApplicantCreateRequest(Applicant, JsonRequestModel):
    birthday: Optional[date] = Field(None, description="Date of birth")
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
    birthday: Optional[date] = Field(None, description="Date of birth")
    social: Optional[List[ApplicantSocial]] = Field(
        None,
        max_items=1,
        description="List of applicant's social accounts",
    )
