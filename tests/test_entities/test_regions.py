from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.regions import Region
from huntflow_api_client.models.response.regions import RegionsListResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
REGIONS_LIST_RESPONSE: Dict[str, Any] = {
    "items": [{"id": 2, "name": "Russian Federation", "order": 1, "parent": 1, "deep": 0}],
    "meta": {"levels": 1, "has_inactive": False},
}


async def test_regions_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/regions",
        json=REGIONS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    regions = Region(api_client)

    response = await regions.list(ACCOUNT_ID)
    assert response == RegionsListResponse(**REGIONS_LIST_RESPONSE)
