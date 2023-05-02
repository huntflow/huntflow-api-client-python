from typing import List, Optional

from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel
from huntflow_api_client.models.utils import descriptions

nested_division_example = [
    {"name": "Division 1.1", "foreign": "d1.1", "meta": {"lead": "test@example.com"}},
]


class Division(JsonRequestModel):
    name: str = Field(..., min_length=1, description="Division name", example="Division 1")
    foreign: str = Field(
        ...,
        min_length=1,
        description=descriptions.foreign,
        example="d1",
    )
    meta: Optional[dict] = Field(
        None,
        description="Arbitrary structure with additional information",
        example={"lead": "director@example.com", "comment": "Main division"},
    )
    items: Optional[List["Division"]] = Field(
        None,
        description="List with subdivisions",
        example=nested_division_example,
    )


class BatchDivisionsRequest(JsonRequestModel):
    items: List[Division]
