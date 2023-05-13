from pydantic import BaseModel, Field


class AccountTagResponse(BaseModel):
    id: int = Field(..., description="Tag ID")
    name: str = Field(..., description="Tag name")
    color: str = Field(..., description="Tag color (HEX format)")
