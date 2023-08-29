from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.organization_settings import OrganizationSettings
from huntflow_api_client.models.response.organization_settings import (
    CloseReasonsListResponse,
    HoldReasonsListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

HOLD_REASONS_RESPONSE: Dict[str, Any] = {"items": [{"id": 20, "name": "Vacancy cancelled"}]}
CLOSE_REASONS_RESPONSE: Dict[str, Any] = {"items": [{"id": 23, "name": "Everyone hired"}]}

ACCOUNT_ID = 1


async def test_get_hold_reasons(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancy_hold_reasons",
        json=HOLD_REASONS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    settings = OrganizationSettings(api_client)

    response = await settings.get_hold_reasons(ACCOUNT_ID)
    assert response == HoldReasonsListResponse(**HOLD_REASONS_RESPONSE)


async def test_get_close_reasons(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancy_close_reasons",
        json=CLOSE_REASONS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    settings = OrganizationSettings(api_client)

    response = await settings.get_close_reasons(ACCOUNT_ID)
    assert response == CloseReasonsListResponse(**CLOSE_REASONS_RESPONSE)
