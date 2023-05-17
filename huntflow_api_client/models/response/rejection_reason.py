from typing import List, Optional

from pydantic import BaseModel, Field


class RejectionReason(BaseModel):
    """The ID can be None because the backend adds the rejection reason "Other" where ID is None"""

    id: Optional[int] = Field(None, description="Rejection reason ID")
    name: str = Field(..., description="Rejection reason name")
    order: int = Field(..., description="Order")


class RejectionReasonsListResponse(BaseModel):
    items: List[RejectionReason]
