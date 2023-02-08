from pydantic import BaseModel, Field


class CreateAccountTagRequest(BaseModel):
    name: str = Field(..., description="Tag name", example="Blacklist")
    color: str = Field(..., description="Tag color (HEX format)", example="000000")
