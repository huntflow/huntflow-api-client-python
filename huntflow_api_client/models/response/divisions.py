from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Division(BaseModel):
    id: int = Field(..., description="Division ID")
    name: str = Field(..., description="Division name")
    order: int = Field(..., description="Order number")
    active: bool = Field(..., description="Activity flag")
    parent: Optional[int] = Field(None, description="Parent division ID")
    deep: int = Field(..., description="Depth level")
    foreign: Optional[str] = Field(
        None,
        description="The unique identifier in the customer's internal system",
    )
    meta: Optional[dict] = Field(
        None,
        description="Additional meta information",
    )


class Meta(BaseModel):
    levels: int = Field(
        ...,
        description="The number of levels of nesting in the structure",
    )
    has_inactive: bool = Field(
        ...,
        description="A flag indicating whether the structure has inactive divisions",
    )


class DivisionsListResponse(BaseModel):
    items: List[Division]
    meta: Meta


class BatchDivisionsPayload(BaseModel):
    task_id: UUID = Field(..., description="Task ID")


class BatchDivisionsMeta(BaseModel):
    data: dict = Field(..., description="Request body content")
    account_id: int = Field(..., description="Organization ID")


class BatchDivisionsResponse(BaseModel):
    status: str = Field(..., description="Operation status")
    payload: BatchDivisionsPayload
    meta: BatchDivisionsMeta
