from pydantic import BaseModel, Field


class AccountTagResponse(BaseModel):
    id: int = Field(..., description="Tag ID", example=10)  # noqa: VNE003 A003
    name: str = Field(..., description="Tag name", example="Blacklist")
    color: str = Field(..., description="Tag color (HEX format)", example="000000")
