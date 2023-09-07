from typing import List, Optional

from pydantic import BaseModel, Field, PositiveInt

from huntflow_api_client.models.common import JsonRequestModel


class ApplicantResumeUpdateData(BaseModel):
    body: Optional[str] = Field(..., description="Resume text")


class ApplicantResumeUpdateRequest(JsonRequestModel):
    account_source: Optional[PositiveInt] = Field(..., description="Resume source ID")
    data: Optional[ApplicantResumeUpdateData] = Field(..., description="Resume data")
    files: Optional[List[PositiveInt]] = Field(
        [],
        max_length=1,
        description="Upload files<br>" "List of file's ID attached to the applicant resume",
    )
