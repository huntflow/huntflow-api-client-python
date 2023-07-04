from typing import List

from pydantic import Field, PositiveInt

from huntflow_api_client.models.common import JsonRequestModel


class ApplicantTagsUpdateRequest(JsonRequestModel):
    tags: List[PositiveInt] = Field(..., description="List of applicant's tags IDs")
