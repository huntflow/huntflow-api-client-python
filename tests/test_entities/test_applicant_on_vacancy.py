from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.applicant_on_vacancy import ApplicantOnVacancy
from huntflow_api_client.models.request.applicant_on_vacancy import (
    AddApplicantToVacancyRequest,
    ApplicantVacancySplitRequest,
    ChangeVacancyApplicantStatusRequest,
)
from huntflow_api_client.models.response.applicant_on_vacancy import (
    AddApplicantToVacancyResponse,
    ApplicantVacancySplitResponse,
    RejectionReasonsListResponse,
    VacancyStatusesResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
APPLICANT_ID = 1
VACANCY_ID = 3
STATUS_ID = 4
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
REJECTION_REASONS_LIST_RESPONSE: Dict[str, Any] = {
    "items": [{"id": 1, "name": "High demands salary", "order": 1}],
}
ATTACH_APPLICANT_TO_VAC_RESPONSE: Dict[str, Any] = {
    "id": ACCOUNT_ID,
    "changed": "2020-01-01T00:00:00+03:00",
    "vacancy": VACANCY_ID,
    "status": STATUS_ID,
    "rejection_reason": 1,
}
ATTACH_APPLICANT_TO_VAC_REQUEST: Dict[str, Any] = {"vacancy": VACANCY_ID, "status": 3}
UPDATE_STATUS_REQUEST: Dict[str, Any] = {"vacancy": VACANCY_ID, "status": STATUS_ID}
UPDATE_STATUS_RESPONSE: Dict[str, Any] = {
    "id": ACCOUNT_ID,
    "changed": "2020-01-01T00:00:00+03:00",
    "vacancy": VACANCY_ID,
    "status": STATUS_ID,
    "rejection_reason": 1,
}
MOVE_APPLICANT_REQUEST: Dict[str, Any] = {"applicant": APPLICANT_ID, "status": 21}
MOVE_APPLICANT_RESPONSE: Dict[str, Any] = {
    "id": 0,
    "applicant": APPLICANT_ID,
    "status": STATUS_ID,
    "vacancy": VACANCY_ID,
    "vacancy_parent": 9,
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
    applicant_statuses = ApplicantOnVacancy(api_client)

    response = await applicant_statuses.list(ACCOUNT_ID)

    assert response == VacancyStatusesResponse(**APPLICANT_ON_VAC_STATUS_LIST_RESPONSE)


async def test_rejection_reasons_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/rejection_reasons",
        json=REJECTION_REASONS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    applicant_statuses = ApplicantOnVacancy(api_client)

    response = await applicant_statuses.rejection_reasons_list(ACCOUNT_ID)

    assert response == RejectionReasonsListResponse(**REJECTION_REASONS_LIST_RESPONSE)


async def test_attach_applicant_to_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/vacancy",
        json=ATTACH_APPLICANT_TO_VAC_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = AddApplicantToVacancyRequest(**ATTACH_APPLICANT_TO_VAC_REQUEST)
    applicant_statuses = ApplicantOnVacancy(api_client)

    response = await applicant_statuses.attach_applicant_to_vacancy(
        ACCOUNT_ID, APPLICANT_ID, api_request,
    )

    assert response == AddApplicantToVacancyResponse(**ATTACH_APPLICANT_TO_VAC_RESPONSE)


async def test_update_vacancy_status_for_applicant(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/vacancy",
        json=UPDATE_STATUS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = ChangeVacancyApplicantStatusRequest(**UPDATE_STATUS_REQUEST)
    applicant_statuses = ApplicantOnVacancy(api_client)

    response = await applicant_statuses.update_vacancy_status_for_applicant(
        ACCOUNT_ID, APPLICANT_ID, api_request,
    )

    assert response == AddApplicantToVacancyResponse(**UPDATE_STATUS_RESPONSE)


async def test_move_applicant_to_child_vacancy(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/vacancy/{VACANCY_ID}/split",
        json=MOVE_APPLICANT_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = ApplicantVacancySplitRequest(**MOVE_APPLICANT_REQUEST)
    applicant_statuses = ApplicantOnVacancy(api_client)

    response = await applicant_statuses.move_applicant_to_child_vacancy(
        ACCOUNT_ID, VACANCY_ID, api_request,
    )

    assert response == ApplicantVacancySplitResponse(**MOVE_APPLICANT_RESPONSE)
