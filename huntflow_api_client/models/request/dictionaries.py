from __future__ import annotations
from typing import Optional, List

from pydantic import BaseModel, constr, Field

from huntflow_api_client.models.common import JsonRequestModel


class DictionaryItem(BaseModel):
    name: constr(min_length=1, max_length=255) = Field(..., description="Dictionary item name")
    foreign: Optional[constr(min_length=1, max_length=1024)] = Field(None, description="Foreign")
    meta: Optional[dict] = Field(
        None,
        description="Meta information",
        example={"latitude": 55.5374, "longitude": 60.1408},
    )
    items: Optional[list[DictionaryItem]] = Field(None, description="Dictionary items")


DictionaryItem.update_forward_refs()


class DictionaryCreateRequest(JsonRequestModel):
    code: constr(min_length=1, max_length=128) = Field(..., description="Dictionary code")
    name: constr(min_length=1, max_length=255) = Field(..., description="Dictionary name")
    foreign: Optional[constr(min_length=1, max_length=1024)] = Field(None, description="Foreign")
    items: List[DictionaryItem] = Field(..., description="Dictionary items")


class DictionaryUpdateRequest(JsonRequestModel):
    name: constr(min_length=1, max_length=255) = Field(..., description="Dictionary name")
    foreign: Optional[constr(min_length=1, max_length=1024)] = Field(None, description="Foreign")
    items: list[DictionaryItem] = Field(..., description="Dictionary items")
