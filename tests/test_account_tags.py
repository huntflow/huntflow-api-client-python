import pytest

from pytest_httpx import HTTPXMock

from tests.conftest import API_URL
from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.tags import AccountTag

from huntflow_api_client.models.response.tags import AccountTagResponse
from huntflow_api_client.models.request.tags import CreateAccountTagRequest


pytestmark = pytest.mark.asyncio


ACCOUNT_ID = 1
TAG_ID = 2

ACCOUNT_TAG_RESPONSE = {
    "color": "00ad3b",
    "id": 34,
    "name": "Blacklist"
}
CREATE_ACCOUNT_TAG_REQUEST = {
    "color": "000000",
    "name": "Whitelist"
}


async def test_get_account_tag(httpx_mock: HTTPXMock, api_client: HuntflowAPI):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        json=ACCOUNT_TAG_RESPONSE
    )
    tags = AccountTag(api_client)

    response = await tags.get(ACCOUNT_ID, TAG_ID)
    assert response == AccountTagResponse(**ACCOUNT_TAG_RESPONSE)


async def test_create_account_tag(httpx_mock: HTTPXMock, api_client: HuntflowAPI):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/tags",
        json=ACCOUNT_TAG_RESPONSE
    )

    api_request = CreateAccountTagRequest(**CREATE_ACCOUNT_TAG_REQUEST)
    tags = AccountTag(api_client)

    response = await tags.create(ACCOUNT_ID, api_request)
    assert response == AccountTagResponse(**ACCOUNT_TAG_RESPONSE)


async def test_update_account_tag(httpx_mock: HTTPXMock, api_client: HuntflowAPI):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        json=ACCOUNT_TAG_RESPONSE
    )

    api_request = CreateAccountTagRequest(**CREATE_ACCOUNT_TAG_REQUEST)
    tags = AccountTag(api_client)

    response = await tags.update(ACCOUNT_ID, TAG_ID, api_request)
    assert response == AccountTagResponse(**ACCOUNT_TAG_RESPONSE)


async def test_delete_applicant(httpx_mock: HTTPXMock, api_client: HuntflowAPI):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        status_code=204
    )
    tags = AccountTag(api_client)

    response = await tags.delete(ACCOUNT_ID, TAG_ID)
    assert response is None
