from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.tags import AccountTag, ApplicantTag
from huntflow_api_client.models.request.tags import (
    CreateAccountTagRequest,
    UpdateApplicantTagsRequest,
)
from huntflow_api_client.models.response.tags import (
    AccountTagResponse,
    AccountTagsListResponse,
    ApplicantTagsListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
TAG_ID = 2
APPLICANT_ID = 3

ACCOUNT_TAG_RESPONSE: Dict[str, Any] = {
    "color": "00ad3b",
    "id": 34,
    "name": "Blacklist",
}
CREATE_ACCOUNT_TAG_REQUEST: Dict[str, str] = {"color": "000000", "name": "Whitelist"}
ACCOUNT_TAGS_LIST_RESPONSE: Dict[str, Any] = {
    "items": [{"id": 10, "name": "Blacklist", "color": "000000"}],
}

APPLICANT_TAGS_LIST_RESPONSE: Dict[str, Any] = {"tags": [1, 2, 3]}
NEW_TAGS = [3, 4, 6]
APPLICANT_TAGS_UPDATE_RESPONSE: Dict[str, Any] = {"tags": NEW_TAGS}


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


async def test_list_account_tag(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/tags",
        json=ACCOUNT_TAGS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    tags = AccountTag(api_client)

    response = await tags.list(ACCOUNT_ID)
    assert response == AccountTagsListResponse(**ACCOUNT_TAGS_LIST_RESPONSE)


async def test_list_applicant_tag(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/tags",
        json=APPLICANT_TAGS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    tags = ApplicantTag(api_client)

    response = await tags.list(ACCOUNT_ID, APPLICANT_ID)
    assert response == ApplicantTagsListResponse(**APPLICANT_TAGS_LIST_RESPONSE)


async def test_update_applicant_tag(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/tags",
        json=APPLICANT_TAGS_UPDATE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    tags = ApplicantTag(api_client)
    data = UpdateApplicantTagsRequest(tags=NEW_TAGS)

    response = await tags.update(ACCOUNT_ID, APPLICANT_ID, data)
    assert response == ApplicantTagsListResponse(**APPLICANT_TAGS_UPDATE_RESPONSE)
