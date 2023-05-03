from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt


class DictionaryTaskResponsePayload(BaseModel):
    task_id: UUID = Field(..., description="Job ID")


class DictionaryTaskResponseMeta(BaseModel):
    data: dict = Field(..., description="Request body")
    account_id: int = Field(..., description="Organization ID")


class DictionaryTaskResponse(BaseModel):
    status: str = Field(..., description="Operation status", example="ok")
    payload: DictionaryTaskResponsePayload
    meta: DictionaryTaskResponseMeta


class DictionaryUpdateResponse(DictionaryTaskResponse):
    pass


class DictionaryCreateResponse(DictionaryTaskResponse):
    pass


class DictionaryItem(BaseModel):
    id: PositiveInt = Field(..., description="Dictionary ID", example=7)  # noqa: A003 VNE003
    code: str = Field(..., description="Dictionary code", example="citizenship")
    name: str = Field(..., description="Dictionary name", example="Citizenship")
    foreign: Optional[str] = Field(
        None, description="The unique identifier in the customer's internal system", example="d_ctz"
    )
    created: datetime = Field(..., description="Date and time of creating a dictionary")


class DictionariesListResponse(BaseModel):
    items: List[DictionaryItem]


class DictionaryField(BaseModel):
    id: int = Field(..., description="Dictionary field ID")  # noqa: A003 VNE003
    name: str = Field(..., description="Dictionary field name")
    order: int = Field(..., description="Order")
    active: bool = Field(..., description="Activity flag")
    parent: Optional[int] = Field(None, description="Parent dictionary field ID")
    deep: int = Field(..., description="Depth level")
    foreign: Optional[str] = Field(
        None, description="The unique identifier in the customer's internal system",
    )
    meta: Optional[dict] = Field(
        None,
        description="Meta information",
        example={"latitude": 55.5374, "longitude": 60.1408},
    )


class DictionaryResponse(BaseModel):
    id: int = Field(..., description="Dictionary ID")  # noqa: A003 VNE003
    code: str = Field(..., description="Dictionary code")
    name: str = Field(..., description="Dictionary name")
    foreign: Optional[str] = Field(
        None, description="The unique identifier in the customer's internal system",
    )
    created: datetime = Field(..., description="Date and time of creating a dictionary")
    dictionary_fields: List[DictionaryField] = Field(
        ...,
        alias="fields",
        description="List of dictionary fields",
    )
