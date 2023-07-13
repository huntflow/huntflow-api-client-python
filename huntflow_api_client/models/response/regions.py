from typing import List, Optional

from pydantic import BaseModel, Field


class Region(BaseModel):
    id: int = Field(..., description="Region ID")
    name: str = Field(..., description="Region name")
    order: int = Field(..., description="Order number")
    parent: Optional[int] = Field(None, description="Parent Region ID")
    deep: int = Field(..., description="Depth level")


class Meta(BaseModel):
    levels: int = Field(..., description="The number of levels of nesting in the structure")
    has_inactive: bool = Field(
        ...,
        description="A flag indicating whether the structure has inactive regions",
    )


class RegionsListResponse(BaseModel):
    items: List[Region]
    meta: Meta
