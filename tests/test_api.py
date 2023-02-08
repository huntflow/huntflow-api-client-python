import pytest

from pytest_httpx import HTTPXMock

from tests.conftest import read_json, API_URL
from huntflow_api_client_python import HuntflowAPI

from huntflow_api_client_python.models.response.tags import AccountTagResponse
from huntflow_api_client_python.models.request.tags import CreateAccountTagRequest


pytestmark = pytest.mark.asyncio


ACCOUNT_ID = 1
TAG_ID = 2


async def test_get_account_tag(httpx_mock: HTTPXMock, api_client: HuntflowAPI):
    api_response = read_json("api_responses/get_account_tag.json")
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        json=api_response
    )

    response = await api_client.get_account_tag(ACCOUNT_ID, TAG_ID)
    assert response == AccountTagResponse(**api_response)


async def test_create_account_tag(httpx_mock: HTTPXMock, api_client: HuntflowAPI):
    api_response = read_json("api_responses/get_account_tag.json")
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/tags",
        json=api_response
    )

    api_request = read_json("api_requests/create_account_tag.json")
    api_request = CreateAccountTagRequest(**api_request)

    response = await api_client.create_account_tag(ACCOUNT_ID, api_request)
    assert response == AccountTagResponse(**api_response)


async def test_update_account_tag(httpx_mock: HTTPXMock, api_client: HuntflowAPI):
    api_response = read_json("api_responses/get_account_tag.json")
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        json=api_response
    )

    api_request = read_json("api_requests/create_account_tag.json")
    api_request = CreateAccountTagRequest(**api_request)

    response = await api_client.update_account_tag(ACCOUNT_ID, TAG_ID, api_request)
    assert response == AccountTagResponse(**api_response)


async def test_delete_applicant(httpx_mock: HTTPXMock, api_client: HuntflowAPI):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/tags/{TAG_ID}",
        status_code=204
    )

    response = await api_client.delete_account_tag(ACCOUNT_ID, TAG_ID)
    assert response is None
