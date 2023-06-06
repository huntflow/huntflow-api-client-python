from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import User
from huntflow_api_client.models.response.users import UserResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
USER_ID = 2

GET_USER_RESPONSE: Dict[str, Any] = {
    "id": 1,
    "name": "John Doe",
    "type": "owner",
    "head": 2,
    "email": "user@example.com",
    "meta": {},
    "permissions": [{"permission": "status", "value": "97", "vacancy": 1}],
}


async def test_get_user(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/users/{USER_ID}",
        json=GET_USER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    users = User(api_client)

    response = await users.get(ACCOUNT_ID, USER_ID)
    assert response == UserResponse(**GET_USER_RESPONSE)
