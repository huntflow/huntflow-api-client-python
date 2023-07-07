from typing import List

from pydantic import Field, PositiveInt

from huntflow_api_client.models.common import JsonRequestModel


class CreateAccountTagRequest(JsonRequestModel):
    name: str = Field(..., description="Tag name")
    color: str = Field(..., description="Tag color (HEX format)")


class UpdateApplicantTagsRequest(JsonRequestModel):
    tags: List[PositiveInt] = Field(..., description="List of applicant's tags IDs")
