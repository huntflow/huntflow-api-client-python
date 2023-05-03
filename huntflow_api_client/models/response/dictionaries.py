from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from huntflow_api_client.models.utils import descriptions


class DictionaryTaskResponsePayload(BaseModel):
    task_id: UUID = Field(..., description="Job ID")


class DictionaryTaskResponseMeta(BaseModel):
    data: dict = Field(..., description="Request body")
    account_id: int = Field(..., description=descriptions.organization_id)


class DictionaryTaskResponse(BaseModel):
    status: str = Field(..., description="Operation status", example="ok")
    payload: DictionaryTaskResponsePayload
    meta: DictionaryTaskResponseMeta


class DictionaryUpdateResponse(DictionaryTaskResponse):
    pass


class DictionaryCreateResponse(DictionaryTaskResponse):
    pass


class DictionaryItem(BaseModel):
    id: PositiveInt = Field(..., description=descriptions.dict_id, example=7)  # noqa: A003 VNE003
    code: str = Field(..., description=descriptions.dict_code, example="citizenship")
    name: str = Field(..., description=descriptions.dict_name, example="Citizenship")
    foreign: Optional[str] = Field(None, description=descriptions.foreign, example="d_ctz")
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
    foreign: Optional[str] = Field(None, description=descriptions.foreign)
    meta: Optional[dict] = Field(
        None,
        description=descriptions.meta,
        example={"latitude": 55.5374, "longitude": 60.1408},
    )


class DictionaryResponse(BaseModel):
    id: int = Field(..., description=descriptions.dict_id)  # noqa: A003 VNE003
    code: str = Field(..., description=descriptions.dict_code)
    name: str = Field(..., description=descriptions.dict_name)
    foreign: Optional[str] = Field(None, description=descriptions.foreign)
    created: datetime = Field(..., description="Date and time of creating a dictionary")
    dictionary_fields: List[DictionaryField] = Field(
        ...,
        alias="fields",
        description="List of dictionary fields",
    )
