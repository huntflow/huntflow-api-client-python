from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from huntflow_api_client.models.utils.fields import DatetimeWithTZ


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
    id: PositiveInt = Field(..., description="Dictionary ID", example=7)
    code: str = Field(..., description="Dictionary code", example="citizenship")
    name: str = Field(..., description="Dictionary name", example="Citizenship")
    foreign: Optional[str] = Field(None, description="descriptions.texts.foreign", example="d_ctz")
    created: DatetimeWithTZ = Field(..., description="Date and time of creating a dictionary")


class DictionariesListResponse(BaseModel):
    items: list[DictionaryItem]


class DictionaryField(BaseModel):
    id: int = Field(..., description="Dictionary field ID")
    name: str = Field(..., description="Dictionary field name")
    order: int = Field(..., description="Order")
    active: bool = Field(..., description="Activity flag")
    parent: Optional[int] = Field(None, description="Parent dictionary field ID")
    deep: int = Field(..., description="Depth level")
    foreign: Optional[str] = Field(None, description="Foreign")
    meta: Optional[dict] = Field(
        None,
        description="Meta information",
        example={"latitude": 55.5374, "longitude": 60.1408},
    )


class DictionaryResponse(BaseModel):
    id: int = Field(..., description="Dictionary ID")
    code: str = Field(..., description="Dictionary code")
    name: str = Field(..., description="Dictionary name")
    foreign: Optional[str] = Field(None, description="Foreign")
    created: DatetimeWithTZ = Field(..., description="Date and time of creating a dictionary")
    dictionary_fields: list[DictionaryField] = Field(
        ..., alias="fields", description="Dictionary fields"
    )
