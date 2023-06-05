from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import ApplicantsQuestionary
from huntflow_api_client.models.request.questionary import QuestionaryRequest
from huntflow_api_client.models.response.questionary import (
    QuestionaryResponse,
    QuestionarySchemaResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
APPLICANT_ID = 2

ORG_QUESTIONARY_RESPONSE: Dict[str, Any] = {
    "citizenship": {
        "type": "dictionary",
        "id": 1,
        "title": "Citizenship",
        "required": False,
        "order": 1,
        "value": None,
        "show_in_profile": True,
        "dictionary": "citizenship",
        "disableAutofill": True,
        "search_filter": True,
        "account": ACCOUNT_ID,
        "search_field": "multi_field_1",
    },
}
QUESTIONARY_RESPONSE: Dict[str, Any] = {
    "citizenship": None,
    "english": {"id": 1, "name": "B1 – middle", "foreign": "B1", "meta": None},
}


async def test_get_organization_questionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/questionary",
        json=ORG_QUESTIONARY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = ApplicantsQuestionary(api_client)

    response = await questionary.get_organization_questionary(ACCOUNT_ID)
    assert response == QuestionarySchemaResponse.parse_obj(ORG_QUESTIONARY_RESPONSE)


async def test_create_questionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/questionary",
        json=QUESTIONARY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = ApplicantsQuestionary(api_client)
    data = QuestionaryRequest.parse_obj({"english": 1})

    response = await questionary.create(ACCOUNT_ID, APPLICANT_ID, data)
    assert response == QuestionaryResponse.parse_obj(QUESTIONARY_RESPONSE)


async def test_get_applicants_questionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/questionary",
        json=QUESTIONARY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = ApplicantsQuestionary(api_client)

    response = await questionary.get(ACCOUNT_ID, APPLICANT_ID)
    assert response == QuestionaryResponse.parse_obj(QUESTIONARY_RESPONSE)


async def test_patch_questionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/questionary",
        json=QUESTIONARY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = ApplicantsQuestionary(api_client)
    data = QuestionaryRequest.parse_obj({"english": 1})

    response = await questionary.patch(ACCOUNT_ID, APPLICANT_ID, data)
    assert response == QuestionaryResponse.parse_obj(QUESTIONARY_RESPONSE)
