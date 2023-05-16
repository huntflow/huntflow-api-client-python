from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt


class DictionaryTaskResponsePayload(BaseModel):
    task_id: UUID = Field(..., description="Task ID")


class DictionaryTaskResponseMeta(BaseModel):
    data: dict = Field(..., description="Request body")
    account_id: int = Field(..., description="Organization ID")


class DictionaryTaskResponse(BaseModel):
    status: str = Field(..., description="Operation status")
    payload: DictionaryTaskResponsePayload
    meta: DictionaryTaskResponseMeta


class DictionaryItem(BaseModel):
    id: PositiveInt = Field(..., description="Dictionary ID")
    code: str = Field(..., description="Dictionary code")
    name: str = Field(..., description="Dictionary name")
    foreign: Optional[str] = Field(
        None,
        description="The unique identifier in the customer's internal system",
    )
    created: datetime = Field(..., description="Date and time of creating a dictionary")


class DictionariesListResponse(BaseModel):
    items: List[DictionaryItem]


class DictionaryField(BaseModel):
    id: int = Field(..., description="Dictionary field ID")
    name: str = Field(..., description="Dictionary field name")
    order: int = Field(..., description="Order")
    active: bool = Field(..., description="Activity flag")
    parent: Optional[int] = Field(None, description="Parent dictionary field ID")
    deep: int = Field(..., description="Depth level")
    foreign: Optional[str] = Field(
        None,
        description="The unique identifier in the customer's internal system",
    )
    meta: Optional[dict] = Field(
        None,
        description="Meta information",
    )


class DictionaryResponse(BaseModel):
    id: int = Field(..., description="Dictionary ID")
    code: str = Field(..., description="Dictionary code")
    name: str = Field(..., description="Dictionary name")
    foreign: Optional[str] = Field(
        None,
        description="The unique identifier in the customer's internal system",
    )
    created: datetime = Field(..., description="Date and time of creating a dictionary")
    fields: List[DictionaryField] = Field(..., description="List of dictionary fields")
