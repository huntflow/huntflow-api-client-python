from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel


class RefreshTokenRequest(JsonRequestModel):
    refresh_token: str = Field(..., description="Refresh token")
