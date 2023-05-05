from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from huntflow_api_client.models.utils import descriptions


class Division(BaseModel):
    id: int = Field(..., description="Division ID", example=2)
    name: str = Field(..., description="Division name", example="IT Department")
    order: int = Field(..., description="Order number", example=1)
    active: bool = Field(..., description="Activity flag")
    parent: Optional[int] = Field(None, description="Parent division ID", example=1)
    deep: int = Field(..., description="Depth level")
    foreign: Optional[str] = Field(
        None,
        description=descriptions.foreign,
        example="it_department",
    )
    meta: Optional[dict] = Field(
        None,
        description="Additional meta information",
        example={"lead": "test@example.com"},
    )


class Meta(BaseModel):
    levels: int = Field(
        ...,
        description="The number of levels of nesting in the structure",
        example=1,
    )
    has_inactive: bool = Field(
        ...,
        description="A flag indicating whether the structure has inactive divisions",
    )


class DivisionsListResponse(BaseModel):
    items: List[Division]
    meta: Meta


class BatchDivisionsPayload(BaseModel):
    task_id: UUID = Field(..., description=descriptions.task_id)


class BatchDivisionsMeta(BaseModel):
    data: dict = Field(..., description="Request body content")
    account_id: int = Field(..., description=descriptions.organization_id, example=11)


class BatchDivisionsResponse(BaseModel):
    status: str = Field(..., description="Operation status", example="ok")
    payload: BatchDivisionsPayload
    meta: BatchDivisionsMeta
