from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import ApplicantResponse
from huntflow_api_client.models.response.applicant_response import ApplicantResponsesListResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL, VERSIONED_BASE_URL

ACCOUNT_ID = 1
APPLICANT_ID = 2

APPLICANT_RESPONSE_LIST_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": 1,
            "foreign": "10",
            "created": "2020-01-01T00:00:00+03:00",
            "applicant_external": 1,
            "vacancy": {
                "id": 12,
                "position": "Developer",
            },
            "vacancy_external": {
                "id": 10,
                "foreign": "10",
            },
        },
    ],
    "next_page_cursor": "string",
}


async def test_applicant_response_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/responses"
        "?count=30",
        status_code=200,
        json=APPLICANT_RESPONSE_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    applicant_response = ApplicantResponse(api_client)

    response = await applicant_response.list(account_id=ACCOUNT_ID, applicant_id=APPLICANT_ID)
    assert response == ApplicantResponsesListResponse.model_validate(
        APPLICANT_RESPONSE_LIST_RESPONSE,
    )
