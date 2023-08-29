from typing import List, Optional

from pydantic import BaseModel, Field


class HoldReason(BaseModel):
    id: Optional[int] = Field(None, description="Reason ID")
    name: str = Field(..., description="Reason name")


class HoldReasonsListResponse(BaseModel):
    items: List[HoldReason]


class CloseReason(BaseModel):
    id: Optional[int] = Field(None, description="Reason ID")
    name: str = Field(..., description="Reason name")


class CloseReasonsListResponse(BaseModel):
    items: List[CloseReason]
