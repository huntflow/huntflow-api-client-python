from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from huntflow_api_client.models.common import JsonRequestModel
from huntflow_api_client.models.utils import descriptions


class DictionaryItem(BaseModel):
    name: str = Field(..., description="Dictionary item name", min_length=1, max_length=255)
    foreign: Optional[str] = Field(
        None,
        description=descriptions.foreign,
        min_length=1,
        max_length=1024,
    )
    meta: Optional[dict] = Field(
        None,
        description=descriptions.meta,
        example={"latitude": 55.5374, "longitude": 60.1408},
    )
    items: Optional[List[DictionaryItem]] = Field(None, description=descriptions.dict_items)


DictionaryItem.update_forward_refs()


class DictionaryCreateRequest(JsonRequestModel):
    code: str = Field(..., description=descriptions.dict_code, min_length=1, max_length=128)
    name: str = Field(..., description=descriptions.dict_name, min_length=1, max_length=255)
    foreign: Optional[str] = Field(
        None,
        description=descriptions.foreign,
        min_length=1,
        max_length=1024,
    )
    items: List[DictionaryItem] = Field(..., description=descriptions.dict_items)


class DictionaryUpdateRequest(JsonRequestModel):
    name: str = Field(..., description=descriptions.dict_name, min_length=1, max_length=255)
    foreign: Optional[str] = Field(
        None,
        description=descriptions.foreign,
        min_length=1,
        max_length=1024,
    )
    items: List[DictionaryItem] = Field(..., description=descriptions.dict_items)
