from typing import List

from pydantic import BaseModel, Field, PositiveInt


class AccountTagResponse(BaseModel):
    id: int = Field(..., description="Tag ID")
    name: str = Field(..., description="Tag name")
    color: str = Field(..., description="Tag color (HEX format)")


class AccountTagsListResponse(BaseModel):
    items: List[AccountTagResponse]


class ApplicantTagsListResponse(BaseModel):
    tags: List[PositiveInt] = Field(..., description="List of applicant's tags IDs")
