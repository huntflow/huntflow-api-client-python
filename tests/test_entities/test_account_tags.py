from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.tags import AccountTag
from huntflow_api_client.models.request.tags import CreateAccountTagRequest
from huntflow_api_client.models.response.tags import AccountTagResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
TAG_ID = 2

ACCOUNT_TAG_RESPONSE: Dict[str, Any] = {
    "color": "00ad3b",
    "id": 34,
    "name": "Blacklist",
}
CREATE_ACCOUNT_TAG_REQUEST: Dict[str, str] = {"color": "000000", "name": "Whitelist"}


async def test_get_account_tag(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        json=ACCOUNT_TAG_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    tags = AccountTag(api_client)

    response = await tags.get(ACCOUNT_ID, TAG_ID)
    assert response == AccountTagResponse(**ACCOUNT_TAG_RESPONSE)


async def test_create_account_tag(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/tags",
        json=ACCOUNT_TAG_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = CreateAccountTagRequest(**CREATE_ACCOUNT_TAG_REQUEST)
    tags = AccountTag(api_client)

    response = await tags.create(ACCOUNT_ID, api_request)
    assert response == AccountTagResponse(**ACCOUNT_TAG_RESPONSE)


async def test_update_account_tag(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        json=ACCOUNT_TAG_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = CreateAccountTagRequest(**CREATE_ACCOUNT_TAG_REQUEST)
    tags = AccountTag(api_client)

    response = await tags.update(ACCOUNT_ID, TAG_ID, api_request)
    assert response == AccountTagResponse(**ACCOUNT_TAG_RESPONSE)


async def test_delete_tag(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        status_code=204,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    tags = AccountTag(api_client)

    response = await tags.delete(ACCOUNT_ID, TAG_ID)  # type: ignore
    assert response is None
