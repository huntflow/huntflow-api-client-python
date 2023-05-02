from __future__ import annotations
from typing import Optional, List

from pydantic import BaseModel, constr, Field

from huntflow_api_client.models.common import JsonRequestModel
from huntflow_api_client.models.utils import descriptions


class DictionaryItem(BaseModel):
    name: constr(min_length=1, max_length=255) = Field(..., description="Dictionary item name")
    foreign: Optional[constr(min_length=1, max_length=1024)] = Field(
        None, description=descriptions.foreign
    )
    meta: Optional[dict] = Field(
        None,
        description=descriptions.meta,
        example={"latitude": 55.5374, "longitude": 60.1408},
    )
    items: Optional[list[DictionaryItem]] = Field(None, description=descriptions.dict_items)


DictionaryItem.update_forward_refs()


class DictionaryCreateRequest(JsonRequestModel):
    code: constr(min_length=1, max_length=128) = Field(..., description=descriptions.dict_code)
    name: constr(min_length=1, max_length=255) = Field(..., description=descriptions.dict_name)
    foreign: Optional[constr(min_length=1, max_length=1024)] = Field(
        None, description=descriptions.foreign
    )
    items: List[DictionaryItem] = Field(..., description=descriptions.dict_items)


class DictionaryUpdateRequest(JsonRequestModel):
    name: constr(min_length=1, max_length=255) = Field(..., description=descriptions.dict_name)
    foreign: Optional[constr(min_length=1, max_length=1024)] = Field(
        None, description=descriptions.foreign
    )
    items: list[DictionaryItem] = Field(..., description=descriptions.dict_items)
