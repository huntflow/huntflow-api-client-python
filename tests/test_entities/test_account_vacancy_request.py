from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.account_vacancy_request import AccountVacancyRequest
from huntflow_api_client.models.response.account_vacancy_request import (
    AccountVacancyRequestResponse,
    AccountVacancyRequestsListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1

VACANCY_REQUEST_SCHEMA = {
    "id": 16,
    "account": 14,
    "name": "",
    "attendee_required": None,
    "attendee_hint": "",
    "active": True,
    "schema": {
        "field4": {
            "id": 144,
            "type": "string",
            "title": "text",
            "required": True,
            "order": 1,
            "key": "field4",
            "account": 14,
            "pass_to_report": True,
        },
        "field3": {
            "id": 145,
            "type": "text",
            "title": "text",
            "required": True,
            "order": 2,
            "key": "text",
            "account": 14,
            "pass_to_report": True,
        },
        "field2": {
            "id": 146,
            "type": "dictionary",
            "title": "text",
            "required": True,
            "order": 3,
            "account": 14,
            "pass_to_report": True,
            "dictionary": "text",
            "vacancy_field": "text",
        },
        "field1": {
            "id": 147,
            "type": "complex",
            "required": True,
            "order": 4,
            "fields": {
                "field1": {
                    "id": 148,
                    "type": "select",
                    "title": "text",
                    "required": True,
                    "order": 5,
                    "values": [],
                    "key": "field",
                    "account": 14,
                    "pass_to_report": True,
                    "vacancy_field": "text",
                },
                "field2": {
                    "id": 149,
                    "type": "string",
                    "title": "text",
                    "required": True,
                    "order": 6,
                    "account": 14,
                    "availableOn": {
                        "type": "field",
                        "operator": "==",
                        "field": "text",
                        "value": "text",
                    },
                },
            },
            "key": "field1",
            "account": 14,
            "delimiter": True,
        },
    },
}

VACANCY_REQUEST_SCHEMAS_LIST = {
    "items": [VACANCY_REQUEST_SCHEMA],
}


async def test_list_schemas(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/account_vacancy_requests?only_active=true",
        json=VACANCY_REQUEST_SCHEMAS_LIST,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancy_request = AccountVacancyRequest(api_client)
    response = await vacancy_request.list(ACCOUNT_ID, only_active=True)
    assert response == AccountVacancyRequestsListResponse.model_validate(
        VACANCY_REQUEST_SCHEMAS_LIST,
    )


async def test_get_schema(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    schema_id = 1
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/account_vacancy_requests/{schema_id}",
        json=VACANCY_REQUEST_SCHEMA,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancy_request = AccountVacancyRequest(api_client)
    response = await vacancy_request.get(ACCOUNT_ID, schema_id)
    assert response == AccountVacancyRequestResponse.model_validate(VACANCY_REQUEST_SCHEMA)
