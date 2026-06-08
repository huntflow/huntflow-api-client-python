from typing import List

from pydantic import BaseModel, Field

from huntflow_api_client.models.consts import InterviewType as InterviewTypeEnum


class InterviewType(BaseModel):
    id: int = Field(..., description="Interview type ID", examples=[20])
    name: str = Field(..., description="Interview type name", examples=["Phone interview"])
    account: int = Field(..., description="Organization ID", examples=[42])
    order: int = Field(..., description="Order number")
    type: InterviewTypeEnum = Field(
        ...,
        description="Type of the interview",
        examples=[InterviewTypeEnum.USER],
    )


class InterviewTypesListResponse(BaseModel):
    items: List[InterviewType]
