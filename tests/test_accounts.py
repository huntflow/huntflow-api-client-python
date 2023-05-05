from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.accounts import Account
from huntflow_api_client.models.response.accounts import (
    MeResponse,
    OrganizationInfoResponse,
    OrganizationsListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
GET_USER_RESPONSE: Dict[str, Any] = {
    "id": 1,
    "name": "API: test",
    "position": None,
    "email": "test1@test.com",
    "phone": None,
    "locale": "ru_RU",
}
ORG_LIST_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": ACCOUNT_ID,
            "name": "Test Name",
            "nick": "test_name",
            "member_type": "owner",
            "production_calendar": 1,
        },
    ],
}
GET_ORG_INFO_RESPONSE: Dict[str, Any] = {
    "id": ACCOUNT_ID,
    "name": "Test Name",
    "nick": "test_name",
    "locale": "ru_RU",
    "photo": None,
}


async def test_get_current_user(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/me",
        json=GET_USER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    accounts = Account(api_client)

    response = await accounts.get_current_user()
    assert response == MeResponse(**GET_USER_RESPONSE)


async def test_available_org_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts",
        json=ORG_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    accounts = Account(api_client)

    response = await accounts.list()
    assert response == OrganizationsListResponse(**ORG_LIST_RESPONSE)


async def test_get_org_info(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}",
        json=GET_ORG_INFO_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    accounts = Account(api_client)

    response = await accounts.get(ACCOUNT_ID)
    assert response == OrganizationInfoResponse(**GET_ORG_INFO_RESPONSE)
