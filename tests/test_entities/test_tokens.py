from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import Token
from huntflow_api_client.models.request.token import RefreshTokenRequest
from huntflow_api_client.models.response.token import RefreshTokenResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL, VERSIONED_BASE_URL

REFRESH_TOKEN_RESPONSE = {
    "access_token": "1234",
    "token_type": "1234",
    "expires_in": 1234,
    "refresh_token_expires_in": 1234,
    "refresh_token": "1234",
}


async def test_refresh_token(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/token/refresh",
        json=REFRESH_TOKEN_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    tags = Token(api_client)

    response = await tags.update(data=RefreshTokenRequest(refresh_token="5678"))
    assert response == RefreshTokenResponse(**REFRESH_TOKEN_RESPONSE)
