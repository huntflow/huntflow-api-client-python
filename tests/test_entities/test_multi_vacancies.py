from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import MultiVacancy
from huntflow_api_client.models.common import FillQuota
from huntflow_api_client.models.request.multi_vacancies import (
    MultiVacancyCreateRequest,
    MultiVacancyPartialUpdateRequest,
    MultiVacancyUpdateRequest,
    VacancyBlock,
    VacancyBlockUpdate,
    VacancyBlockUpdatePartial,
)
from huntflow_api_client.models.response.muilti_vacancies import MultiVacancyResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
VACANCY_ID = 2
MULTI_VACANCY_RESPONSE: Dict[str, Any] = {"task_id": "18945061-87e0-4000-855b-75a663ae5301"}


async def test_create_multi_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/multi-vacancies",
        json=MULTI_VACANCY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    multi_vacancies = MultiVacancy(api_client)
    data = MultiVacancyCreateRequest(
        account_applicant_offer=1,
        position="Test vacancy",
        blocks=[VacancyBlock(fill_quotas=[FillQuota()])],
    )

    response = await multi_vacancies.create(ACCOUNT_ID, data)
    assert response == MultiVacancyResponse(**MULTI_VACANCY_RESPONSE)


async def test_update_multi_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/multi-vacancies/{VACANCY_ID}",
        json=MULTI_VACANCY_RESPONSE,
        method="PUT",
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    multi_vacancies = MultiVacancy(api_client)
    data = MultiVacancyUpdateRequest(
        position="Test vacancy",
        blocks=[VacancyBlockUpdate(fill_quotas=[FillQuota()])],
    )

    response = await multi_vacancies.update(ACCOUNT_ID, VACANCY_ID, data)
    assert response == MultiVacancyResponse(**MULTI_VACANCY_RESPONSE)


async def test_partial_update_multi_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/multi-vacancies/{VACANCY_ID}",
        json=MULTI_VACANCY_RESPONSE,
        method="PATCH",
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    multi_vacancies = MultiVacancy(api_client)
    data = MultiVacancyPartialUpdateRequest(
        position="Test vacancy",
        blocks=[VacancyBlockUpdatePartial()],
    )

    response = await multi_vacancies.update(
        account_id=ACCOUNT_ID,
        vacancy_id=VACANCY_ID,
        data=data,
        partial=True,
    )
    assert response == MultiVacancyResponse(**MULTI_VACANCY_RESPONSE)
