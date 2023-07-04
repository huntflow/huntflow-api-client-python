from typing import List

from pydantic import BaseModel, Field, PositiveInt


class ApplicantTagsListResponse(BaseModel):
    tags: List[PositiveInt] = Field(..., description="List of applicant's tags IDs")
