from typing import List, Optional

from pydantic import BaseModel, Field

from huntflow_api_client.models.common import JsonRequestModel


class DictionaryItem(BaseModel):
    name: str = Field(..., description="Dictionary item name", min_length=1, max_length=255)
    foreign: Optional[str] = Field(
        None,
        description="The unique identifier in the customer's internal system",
        min_length=1,
        max_length=1024,
    )
    meta: Optional[dict] = Field(None, description="Meta information")
    items: Optional[List["DictionaryItem"]] = Field(None, description="Dictionary items")


class DictionaryCreateRequest(JsonRequestModel):
    code: str = Field(..., description="Dictionary code", min_length=1, max_length=128)
    name: str = Field(..., description="Dictionary name", min_length=1, max_length=255)
    foreign: Optional[str] = Field(
        None,
        description="The unique identifier in the customer's internal system",
        min_length=1,
        max_length=1024,
    )
    items: List[DictionaryItem] = Field(..., description="Dictionary items")


class DictionaryUpdateRequest(JsonRequestModel):
    name: str = Field(..., description="Dictionary name", min_length=1, max_length=255)
    foreign: Optional[str] = Field(
        None,
        description="The unique identifier in the customer's internal system",
        min_length=1,
        max_length=1024,
    )
    items: List[DictionaryItem] = Field(..., description="Dictionary items")
