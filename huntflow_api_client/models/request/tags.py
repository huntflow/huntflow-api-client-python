from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel


class CreateAccountTagRequest(JsonRequestModel):
    name: str = Field(..., description="Tag name", example="Blacklist")
    color: str = Field(..., description="Tag color (HEX format)", example="000000")
