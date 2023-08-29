from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.organization_settings import OrganizationSettings
from huntflow_api_client.models.response.organization_settings import (
    BaseSurveySchemaTypeWithSchemas,
    CloseReasonsListResponse,
    HoldReasonsListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
SURVEY_ID = 2

HOLD_REASONS_RESPONSE: Dict[str, Any] = {"items": [{"id": 20, "name": "Vacancy cancelled"}]}
CLOSE_REASONS_RESPONSE: Dict[str, Any] = {"items": [{"id": 23, "name": "Everyone hired"}]}
SURVEY_FORM_RESPONSE: Dict[str, Any] = {
    "id": 1,
    "name": "test_survey",
    "type": "type_a",
    "active": True,
    "created": "2020-01-01T00:00:00+03:00",
    "updated": "2020-01-01T00:00:00+03:00",
    "schema": {},
    "ui_schema": {},
}


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


async def test_get_applicant_survey_form(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_a/{SURVEY_ID}",
        json=SURVEY_FORM_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    settings = OrganizationSettings(api_client)

    response = await settings.get_applicant_survey_form(ACCOUNT_ID, SURVEY_ID)
    assert response == BaseSurveySchemaTypeWithSchemas(**SURVEY_FORM_RESPONSE)
