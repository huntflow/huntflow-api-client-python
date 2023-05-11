from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.vacancy_requests import VacancyRequest
from huntflow_api_client.models.request.vacancy_requests import CreateVacancyRequestRequest
from huntflow_api_client.models.response.account_vacancy_request import (
    AccountVacancyRequestResponse,
    AccountVacancyRequestsListResponse,
)
from huntflow_api_client.models.response.vacancy_requests import (
    VacancyRequestListResponse,
    VacancyRequestResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1

VACANCY_REQUEST_LIST_WITHOUT_VALUES = {
    "page": 1,
    "count": 30,
    "total_pages": 1,
    "total_items": 1,
    "items": [
        {
            "id": 1,
            "position": "1",
            "status": "approved",
            "account_vacancy_request": 1,
            "created": "2023-05-03T12:02:03+03:00",
            "updated": "2023-05-03T12:02:03+03:00",
            "changed": None,
            "vacancy": None,
            "creator": {"id": 1, "name": "test@example.com", "email": "test@example.com"},
            "states": [],
        },
    ],
}

VACANCY_REQUEST_RESPONSE = {
    "id": 1,
    "position": "1",
    "status": "approved",
    "account_vacancy_request": 1,
    "created": "2023-05-03T12:02:03+03:00",
    "updated": "2023-05-03T12:02:03+03:00",
    "changed": None,
    "vacancy": None,
    "creator": {"id": 1, "name": "test@example.com", "email": "test@example.com"},
    "states": [],
    "values": {
        "position": "1",
        "account_division": 1,
        "category": 1,
        "_reason": {"reason": "Новая позиция", "reason_replacement": None},
        "money": "text",
        "requirements": "<p>text</p>",
        "body": "<p>text</p>",
        "deadline": "03.05.2023",
        "calc_deadline": None,
    },
}
VACANCY_REQUEST_LIST_WITH_VALUES = {
    "page": 1,
    "count": 30,
    "total_pages": 1,
    "total_items": 1,
    "items": [],
}

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
VACANCY_REQUEST_LIST_WITH_VALUES["items"].append(VACANCY_REQUEST_RESPONSE)  # type: ignore

VACANCY_REQUEST_CREATE_REQUEST = {
    "account_vacancy_request": 1,
    "position": "1",
    "applicants_to_hire": 1,
}


async def test_list_vacancy_request(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancy_requests?page=1&&count=30&&values=false",
        json=VACANCY_REQUEST_LIST_WITHOUT_VALUES,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancy_request = VacancyRequest(api_client)

    response = await vacancy_request.list(ACCOUNT_ID)
    assert response == VacancyRequestListResponse.parse_obj(VACANCY_REQUEST_LIST_WITHOUT_VALUES)

    httpx_mock.add_response(
        url=(
            f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancy_requests?"
            f"vacancy_id=1&&page=1&&count=30&&values=true"
        ),
        json=VACANCY_REQUEST_LIST_WITH_VALUES,
    )

    response = await vacancy_request.list(ACCOUNT_ID, vacancy_id=1, values=True)
    assert response == VacancyRequestListResponse.parse_obj(VACANCY_REQUEST_LIST_WITH_VALUES)


async def test_get_vacancy_request(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancy_requests/1",
        json=VACANCY_REQUEST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancy_request = VacancyRequest(api_client)

    response = await vacancy_request.get(ACCOUNT_ID, 1)
    assert response == VacancyRequestResponse.parse_obj(VACANCY_REQUEST_RESPONSE)
    assert response.values


async def test_create_vacancy_request(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancy_requests",
        json=VACANCY_REQUEST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancy_request = VacancyRequest(api_client)
    data = CreateVacancyRequestRequest.parse_obj(VACANCY_REQUEST_CREATE_REQUEST)
    response = await vacancy_request.create(ACCOUNT_ID, data)
    assert response == VacancyRequestResponse.parse_obj(VACANCY_REQUEST_RESPONSE)


async def test_list_schemas(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/account_vacancy_requests?only_active=true",
        json=VACANCY_REQUEST_SCHEMAS_LIST,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancy_request = VacancyRequest(api_client)
    response = await vacancy_request.list_schemas(ACCOUNT_ID, only_active=True)
    assert response == AccountVacancyRequestsListResponse.parse_obj(VACANCY_REQUEST_SCHEMAS_LIST)


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
    vacancy_request = VacancyRequest(api_client)
    response = await vacancy_request.get_schema(ACCOUNT_ID, schema_id)
    assert response == AccountVacancyRequestResponse.parse_obj(VACANCY_REQUEST_SCHEMA)
