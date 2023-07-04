from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.applicant_tags import ApplicantTag
from huntflow_api_client.models.request.applicant_tags import ApplicantTagsUpdateRequest
from huntflow_api_client.models.response.applicant_tags import ApplicantTagsListResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
APPLICANT_ID = 2

APPLICANT_TAGS_LIST_RESPONSE: Dict[str, Any] = {"tags": [1, 2, 3]}
NEW_TAGS = [3, 4, 6]
APPLICANT_TAGS_UPDATE_RESPONSE: Dict[str, Any] = {"tags": NEW_TAGS}


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
    data = ApplicantTagsUpdateRequest(tags=NEW_TAGS)

    response = await tags.update(ACCOUNT_ID, APPLICANT_ID, data)
    assert response == ApplicantTagsListResponse(**APPLICANT_TAGS_UPDATE_RESPONSE)
