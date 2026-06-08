from datetime import datetime

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.recommendation import Recommendation
from huntflow_api_client.models.consts import RecommendationProcessingStatus
from huntflow_api_client.models.response.recommendation import RecommendationListResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL, VERSIONED_BASE_URL

ACCOUNT_ID = 1
VACANCY_ID = 2
RECOMMENDATION_LIST_RESPONSE = {
    "items": [
        {
            "id": 3,
            "vacancy_id": VACANCY_ID,
            "applicant_id": 4,
            "rank": 5,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "resolved_by_user": 6,
            "status": "TAKEN",
        },
    ],
    "next_page_cursor": "any",
}


async def test_list_recommendation(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=(
            f"{VERSIONED_BASE_URL}/accounts/{ACCOUNT_ID}/recommendations/{VACANCY_ID}"
            f"?count=1&processing_status=PROCESSED"
        ),
        json=RECOMMENDATION_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    recommendations = Recommendation(api_client)

    response = await recommendations.list(
        ACCOUNT_ID,
        VACANCY_ID,
        count=1,
        processing_status=RecommendationProcessingStatus.PROCESSED,
    )
    assert response == RecommendationListResponse.model_validate(RECOMMENDATION_LIST_RESPONSE)

    next_page_cursor = "cursor"
    httpx_mock.add_response(
        url=(
            f"{VERSIONED_BASE_URL}/accounts/{ACCOUNT_ID}/recommendations/{VACANCY_ID}"
            f"?next_page_cursor={next_page_cursor}&processing_status=ALL"
        ),
        json=RECOMMENDATION_LIST_RESPONSE,
    )
    response = await recommendations.list(ACCOUNT_ID, VACANCY_ID, next_page_cursor=next_page_cursor)
    assert response == RecommendationListResponse.model_validate(RECOMMENDATION_LIST_RESPONSE)
