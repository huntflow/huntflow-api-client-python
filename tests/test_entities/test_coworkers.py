from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.coworkers import Coworker
from huntflow_api_client.models.response.coworkers import CoworkerResponse, CoworkersListResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
COWORKER_ID = 2
VACANCY_ID = 3
GET_COWORKER_RESPONSE: Dict[str, Any] = {
    "id": COWORKER_ID,
    "member": 1,
    "name": "Test Name",
    "type": "watcher",
    "head": None,
    "email": "test@test.com",
    "meta": None,
    "permissions": [
        {"permission": "vacancy", "value": None, "vacancy": VACANCY_ID},
        {"permission": "status", "value": "1", "vacancy": VACANCY_ID},
        {"permission": "status", "value": "2", "vacancy": VACANCY_ID},
        {"permission": "status", "value": "3", "vacancy": VACANCY_ID},
    ],
}
GET_COWORKER_LIST_RESPONSE: Dict[str, Any] = {
    "page": 1,
    "count": 30,
    "total_pages": 1,
    "total_items": 3,
    "items": [
        {
            "id": ACCOUNT_ID,
            "member": 1,
            "name": "test-1@test.com",
            "type": "owner",
            "head": None,
            "email": "test-1@test.com",
            "meta": None,
            "permissions": [],
        },
        {
            "id": 2,
            "member": 2,
            "name": "Test Name",
            "type": "owner",
            "head": None,
            "email": "test-2@test.com",
            "meta": None,
            "permissions": [],
        },
        {
            "id": 3,
            "member": 3,
            "name": "Second Test Name",
            "type": "watcher",
            "head": None,
            "email": "test-3@test.com",
            "meta": None,
            "permissions": [],
        },
    ],
}


async def test_get(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/coworkers?vacancy_id={VACANCY_ID}",
        json=GET_COWORKER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    coworkers = Coworker(api_client)

    response = await coworkers.get(ACCOUNT_ID, COWORKER_ID, VACANCY_ID)

    assert response == CoworkerResponse(**GET_COWORKER_RESPONSE)


async def test_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/coworkers?count=30&page=1",
        json=GET_COWORKER_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    coworkers = Coworker(api_client)

    response = await coworkers.list(ACCOUNT_ID)

    assert response == CoworkersListResponse(**GET_COWORKER_LIST_RESPONSE)
