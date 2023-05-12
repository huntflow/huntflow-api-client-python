import datetime
from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.vacancies import Vacancy
from huntflow_api_client.models.common import EditedFillQuota, FillQuota, StatusResponse
from huntflow_api_client.models.request.vacancies import (
    VacancyCreateRequest,
    VacancyListState,
    VacancyMemberCreateRequest,
    VacancyUpdatePartialRequest,
    VacancyUpdateRequest,
)
from huntflow_api_client.models.response.vacancies import (
    AdditionalFieldsSchemaResponse,
    VacancyCreateResponse,
    VacancyListResponse,
    VacancyResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
VACANCY_ID = 2
COWORKER_ID = 3

GET_ORG_ADD_FIELDS_SCHEMA_RESPONSE: Dict[str, Any] = {
    "responsible_recruiter": {
        "id": 1,
        "type": "dictionary",
        "title": "Test recruiter",
        "required": True,
        "order": 1,
        "value": None,
        "pass_to_report": True,
        "name": "responsible_recruiter",
        "dictionary": "recruiter",
        "search_field": "multi_field_2",
        "filterable": True,
        "disableAutofill": True,
        "account": ACCOUNT_ID,
    },
    "manager": {
        "id": 1,
        "type": "dictionary",
        "title": "Test manager",
        "required": True,
        "order": 2,
        "value": None,
        "pass_to_report": False,
        "name": "manager",
        "dictionary": "employee",
        "search_field": "multi_field_3",
        "filterable": True,
        "disableAutofill": True,
        "account": ACCOUNT_ID,
    },
}
GET_LIST_VACANCIES_RESPONSE: Dict[str, Any] = {
    "page": 1,
    "count": 30,
    "total_pages": 1,
    "total_items": 1,
    "items": [
        {
            "account_division": None,
            "account_region": None,
            "position": "Manager",
            "company": None,
            "money": "1000",
            "priority": 0,
            "hidden": False,
            "state": "OPEN",
            "id": 1,
            "created": "2023-05-04T12:18:59+03:00",
            "additional_fields_list": [],
            "multiple": False,
            "parent": None,
            "account_vacancy_status_group": None,
        },
        {
            "account_division": None,
            "account_region": None,
            "position": "Director",
            "company": None,
            "money": "1000",
            "priority": 0,
            "hidden": False,
            "state": "OPEN",
            "id": 2,
            "created": "2023-04-04T12:18:59+03:00",
            "additional_fields_list": [],
            "multiple": False,
            "parent": None,
            "account_vacancy_status_group": None,
        },
    ],
}
GET_VACANCY_RESPONSE: Dict[str, Any] = {
    "account_division": None,
    "account_region": None,
    "position": "Manager",
    "company": None,
    "money": "7878rub",
    "priority": 0,
    "hidden": False,
    "state": "OPEN",
    "id": 177,
    "created": "2023-05-04T12:18:59+03:00",
    "additional_fields_list": [],
    "multiple": False,
    "parent": None,
    "account_vacancy_status_group": None,
    "updated": "2023-05-04T12:27:50+03:00",
    "body": None,
    "requirements": None,
    "conditions": None,
    "files": [],
    "source": None,
    "blocks": [],
}
CREATE_VACANCY_RESPONSE: Dict[str, Any] = {
    "account_division": None,
    "account_region": None,
    "position": "Developer",
    "company": None,
    "money": None,
    "priority": 0,
    "hidden": False,
    "state": "OPEN",
    "id": 1,
    "created": "2023-05-04T13:06:15+03:00",
    "coworkers": [],
    "body": None,
    "requirements": None,
    "conditions": None,
    "files": [],
    "account_vacancy_status_group": None,
    "parent": None,
    "source": None,
    "multiple": False,
    "vacancy_request": None,
}
PATCH_VACANCY_RESPONSE: Dict[str, Any] = {
    "account_division": None,
    "account_region": None,
    "position": "Developer",
    "company": None,
    "money": "99999999",
    "priority": 0,
    "hidden": False,
    "state": "OPEN",
    "id": 1,
    "created": "2023-05-04T13:06:15+03:00",
    "coworkers": [],
    "body": None,
    "requirements": None,
    "conditions": None,
    "files": [],
    "account_vacancy_status_group": None,
    "parent": None,
    "source": None,
    "multiple": False,
    "vacancy_request": None,
}
UPDATE_VACANCY_RESPONSE: Dict[str, Any] = {
    "account_division": None,
    "account_region": None,
    "position": "Developer",
    "company": None,
    "money": "$100000000",
    "priority": 0,
    "hidden": False,
    "state": "OPEN",
    "id": 1,
    "created": "2023-05-04T13:06:15+03:00",
    "coworkers": [],
    "body": None,
    "requirements": None,
    "conditions": None,
    "files": [],
    "account_vacancy_status_group": None,
    "parent": None,
    "source": None,
    "multiple": False,
    "vacancy_request": None,
}
ASSIGN_COWORKER_RESPONSE: Dict[str, Any] = {"status": True}
ASSIGN_COWORKER_REQUEST: Dict[str, Any] = {
    "permissions": [
        {"permission": "status", "value": 1},
        {"permission": "status", "value": 2},
    ],
}


async def test_get_get_org_vacancy_additional_fields_schema(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies/additional_fields",
        json=GET_ORG_ADD_FIELDS_SCHEMA_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)

    response = await vacancies.get_additional_fields_schema(ACCOUNT_ID)
    assert response == AdditionalFieldsSchemaResponse(**GET_ORG_ADD_FIELDS_SCHEMA_RESPONSE)


async def test_list_vacancies(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies?"
        f"count=30&page=1&mine=false&state=OPEN&state=HOLD",
        json=GET_LIST_VACANCIES_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)

    state = [VacancyListState.OPEN.value, VacancyListState.HOLD.value]
    response = await vacancies.list(account_id=ACCOUNT_ID, state=state)
    assert response == VacancyListResponse(**GET_LIST_VACANCIES_RESPONSE)


async def test_get_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies/{VACANCY_ID}",
        json=GET_VACANCY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)

    response = await vacancies.get(ACCOUNT_ID, VACANCY_ID)
    assert response == VacancyResponse(**GET_VACANCY_RESPONSE)


async def test_create_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies",
        json=CREATE_VACANCY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)

    data = VacancyCreateRequest(  # type: ignore
        position="Developer",
        fill_quotas=[
            FillQuota(  # type: ignore
                deadline=datetime.date(2023, 7, 1),
                applicants_to_hire=1,
            ),
        ],
    )
    response = await vacancies.create(ACCOUNT_ID, data)
    assert response == VacancyCreateResponse(**CREATE_VACANCY_RESPONSE)


async def test_update_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies/{VACANCY_ID}",
        json=UPDATE_VACANCY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)

    data = VacancyUpdateRequest(  # type: ignore
        position="Manager",
        money="99999999",
        fill_quotas=[EditedFillQuota(id=1)],  # type: ignore
    )
    response = await vacancies.update(ACCOUNT_ID, VACANCY_ID, data)
    assert response == VacancyResponse(**UPDATE_VACANCY_RESPONSE)


async def test_delete_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies/{VACANCY_ID}",
        status_code=204,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)

    await vacancies.delete(ACCOUNT_ID, VACANCY_ID)


async def test_patch_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies/{VACANCY_ID}",
        json=PATCH_VACANCY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)

    data = VacancyUpdatePartialRequest(  # type: ignore
        money="$100000000",
    )
    response = await vacancies.patch(ACCOUNT_ID, VACANCY_ID, data)
    assert response == VacancyResponse(**PATCH_VACANCY_RESPONSE)


async def test_assign_coworker(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies/{VACANCY_ID}/members/{COWORKER_ID}",
        json=ASSIGN_COWORKER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)
    data = VacancyMemberCreateRequest(**ASSIGN_COWORKER_REQUEST)

    response = await vacancies.assign_coworker(ACCOUNT_ID, VACANCY_ID, COWORKER_ID, data)
    assert response == StatusResponse(**ASSIGN_COWORKER_RESPONSE)


async def test_remove_coworker(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies/{VACANCY_ID}/members/{COWORKER_ID}",
        status_code=204,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    vacancies = Vacancy(api_client)

    await vacancies.remove_coworker(ACCOUNT_ID, VACANCY_ID, COWORKER_ID)
