from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.rejection_reason import RejectionReason
from huntflow_api_client.models.response.rejection_reason import RejectionReasonsListResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
REJECTION_REASONS_LIST_RESPONSE: Dict[str, Any] = {
    "items": [{"id": 1, "name": "High demands salary", "order": 1}],
}


async def test_rejection_reasons_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/rejection_reasons",
        json=REJECTION_REASONS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    applicant_statuses = RejectionReason(api_client)

    response = await applicant_statuses.list(ACCOUNT_ID)

    assert response == RejectionReasonsListResponse(**REJECTION_REASONS_LIST_RESPONSE)
