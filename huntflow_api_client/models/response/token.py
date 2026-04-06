from pydantic import BaseModel, Field


class RefreshTokenResponse(BaseModel):
    access_token: str = Field(..., description="New access token")
    token_type: str = Field(..., description="Token type")
    expires_in: int = Field(..., description="Token lifetime in seconds")
    refresh_token_expires_in: int = Field(
        ...,
        description="Refresh token lifetime in seconds",
    )
    refresh_token: str = Field(..., description="New refresh token")
