from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.applicant_on_vacancy_status import ApplicantOnVacancyStatus
from huntflow_api_client.models.response.applicant_on_vacancy_status import VacancyStatusesResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
APPLICANT_ON_VAC_STATUS_LIST_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": 1,
            "type": "user",
            "name": "New Lead",
            "removed": "2020-01-01T00:00:00+03:00",
            "order": 0,
            "stay_duration": 10,
        },
    ],
}


async def test_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/vacancies/statuses",
        json=APPLICANT_ON_VAC_STATUS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    statuses = ApplicantOnVacancyStatus(api_client)

    response = await statuses.list(ACCOUNT_ID)

    assert response == VacancyStatusesResponse(**APPLICANT_ON_VAC_STATUS_LIST_RESPONSE)
