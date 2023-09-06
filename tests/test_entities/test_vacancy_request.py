from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.vacancy_requests import VacancyRequest
from huntflow_api_client.models.request.vacancy_requests import CreateVacancyRequestRequest
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
            "creator": {
                "id": 1,
                "name": "test@example.com",
                "email": "test@example.com",
            },
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
    assert response == VacancyRequestListResponse.model_validate(
        VACANCY_REQUEST_LIST_WITHOUT_VALUES,
    )

    httpx_mock.add_response(
        url=(
            f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancy_requests?"
            f"vacancy_id=1&&page=1&&count=30&&values=true"
        ),
        json=VACANCY_REQUEST_LIST_WITH_VALUES,
    )

    response = await vacancy_request.list(ACCOUNT_ID, vacancy_id=1, values=True)
    assert response == VacancyRequestListResponse.model_validate(VACANCY_REQUEST_LIST_WITH_VALUES)


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
    assert response == VacancyRequestResponse.model_validate(VACANCY_REQUEST_RESPONSE)
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
    data = CreateVacancyRequestRequest.model_validate(VACANCY_REQUEST_CREATE_REQUEST)
    response = await vacancy_request.create(ACCOUNT_ID, data)
    assert response == VacancyRequestResponse.model_validate(VACANCY_REQUEST_RESPONSE)
