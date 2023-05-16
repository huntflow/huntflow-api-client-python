from typing import List, Optional

from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel


class Division(JsonRequestModel):
    name: str = Field(..., min_length=1, description="Division name")
    foreign: str = Field(
        ...,
        min_length=1,
        description="The unique identifier in the customer's internal system",
    )
    meta: Optional[dict] = Field(
        None,
        description="Arbitrary structure with additional information",
    )
    items: Optional[List["Division"]] = Field(
        None,
        description="List with subdivisions",
    )


class BatchDivisionsRequest(JsonRequestModel):
    items: List[Division]
