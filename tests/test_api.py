import pytest

from pytest_httpx import HTTPXMock

from tests.conftest import read_json, API_URL
from huntflow_api_client_python.api import HuntflowApi
from huntflow_api_client_python.serializers.response.info import OrganizationInfoResponse
from huntflow_api_client_python.serializers.response.applicants import (
    ApplicantCreateResponse,
    ApplicantUpdateResponse,
    ApplicantVacancySplitResponse
)
from huntflow_api_client_python.serializers.request.applicants import (
    ApplicantCreateRequest,
    ApplicantUpdateRequest,
    ApplicantVacancySplitRequest
)


pytestmark = pytest.mark.asyncio


ACCOUNT_ID = 1
APPLICANT_ID = 2
VACANCY_ID = 3


async def test_get_organization(httpx_mock: HTTPXMock, api_client: HuntflowApi):
    api_response = read_json("api_responses/get_organization_info.json")
    httpx_mock.add_response(url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}", json=api_response)

    response = await api_client.get_organization(ACCOUNT_ID)
    assert response == OrganizationInfoResponse(**api_response)


async def test_create_applicant(httpx_mock: HTTPXMock, api_client: HuntflowApi):
    api_response = read_json("api_responses/create_applicant.json")
    httpx_mock.add_response(url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/applicants", json=api_response)

    api_request = read_json("api_requests/create_applicant.json")
    api_request = ApplicantCreateRequest(**api_request)

    response = await api_client.create_applicant(ACCOUNT_ID, api_request)
    assert response == ApplicantCreateResponse(**api_response)


async def test_update_applicant(httpx_mock: HTTPXMock, api_client: HuntflowApi):
    api_response = read_json("api_responses/get_applicant.json")
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}",
        json=api_response
    )

    api_request = {"first_name": "John", "money": "100500"}
    api_request = ApplicantUpdateRequest(**api_request)

    response = await api_client.update_applicant(ACCOUNT_ID, APPLICANT_ID, api_request)
    assert response == ApplicantUpdateResponse(**api_response)


async def test_delete_applicant(httpx_mock: HTTPXMock, api_client: HuntflowApi):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}",
        status_code=204
    )

    response = await api_client.delete_applicant(ACCOUNT_ID, APPLICANT_ID)
    assert response is None


async def test_split_applicant_to_vacancy(httpx_mock: HTTPXMock, api_client: HuntflowApi):
    api_response = {
        "id": 8,
        "applicant": 31,
        "status": 94,
        "vacancy": VACANCY_ID,
        "vacancy_parent": 2,
    }
    httpx_mock.add_response(
        url=f"{API_URL}/v2/accounts/{ACCOUNT_ID}/applicants/vacancy/{VACANCY_ID}/split",
        json=api_response
    )

    api_request = {"applicant": 31, "status": 94}
    api_request = ApplicantVacancySplitRequest(**api_request)

    response = await api_client.split_applicant_to_vacancy(ACCOUNT_ID, VACANCY_ID, api_request)
    assert response == ApplicantVacancySplitResponse(**api_response)
