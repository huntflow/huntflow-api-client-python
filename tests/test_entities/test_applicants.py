from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.applicants import Applicant
from huntflow_api_client.models.request.applicants import (
    ApplicantCreateRequest,
    ApplicantUpdateRequest,
)
from huntflow_api_client.models.response.applicants import (
    ApplicantCreateResponse,
    ApplicantItem,
    ApplicantListResponse,
    ApplicantSearchByCursorResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
APPLICANT_ID = 2

APPLICANT_LIST_RESPONSE: Dict[str, Any] = {
    "page": 1,
    "count": 30,
    "total_pages": 1,
    "total_items": 2,
    "items": [
        {
            "first_name": "John",
            "last_name": None,
            "middle_name": None,
            "money": None,
            "phone": None,
            "email": None,
            "skype": None,
            "position": None,
            "company": None,
            "photo": None,
            "id": 1,
            "account": ACCOUNT_ID,
            "photo_url": None,
            "birthday": None,
            "created": "2023-05-10T15:13:15+03:00",
            "tags": [],
            "links": [],
            "external": [
                {
                    "id": 1,
                    "auth_type": "NATIVE",
                    "account_source": None,
                    "updated": "2023-05-10T15:13:15+03:00",
                },
            ],
            "agreement": None,
            "doubles": [],
            "social": [],
        },
        {
            "first_name": "Test",
            "last_name": "Test",
            "middle_name": "Test",
            "money": None,
            "phone": None,
            "email": None,
            "skype": None,
            "position": None,
            "company": None,
            "photo": None,
            "id": 2,
            "account": ACCOUNT_ID,
            "photo_url": None,
            "birthday": None,
            "created": "2023-05-10T10:46:39+03:00",
            "tags": [],
            "links": [
                {
                    "id": 2,
                    "status": 1,
                    "updated": "2023-05-10T10:47:17+03:00",
                    "changed": "2023-05-10T10:47:17+03:00",
                    "vacancy": 3,
                },
            ],
            "external": [
                {
                    "id": 1,
                    "auth_type": "NATIVE",
                    "account_source": None,
                    "updated": "2023-05-10T10:46:39+03:00",
                },
            ],
            "agreement": {"state": None, "decision_date": None},
            "doubles": [],
            "social": [],
        },
    ],
}
APPLICANT_GET_RESPONSE: Dict[str, Any] = {
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Michael",
    "money": "$100000",
    "phone": "89999999999",
    "email": "user@example.com",
    "skype": "my_skype",
    "position": "Front-end developer",
    "company": "Google Inc.",
    "photo": 1,
    "id": 1,
    "account": 5,
    "photo_url": "https://some.photo/12341234",
    "birthday": "2020-01-01",
    "created": "2020-01-01T00:00:00+03:00",
    "tags": [{"tag": 1, "id": 1}],
    "links": [
        {
            "id": 7,
            "status": 12,
            "updated": "2020-01-01T00:00:00+03:00",
            "changed": "2020-01-01T00:00:00+03:00",
            "vacancy": 4,
        },
    ],
    "external": [
        {
            "id": 1,
            "auth_type": "Auth",
            "account_source": 10,
            "updated": "2020-01-01T00:00:00+03:00",
        },
    ],
    "agreement": {"state": None, "decision_date": None},
    "doubles": [{"double": 8}],
    "social": [
        {
            "id": 1,
            "social_type": "TELEGRAM",
            "value": "TelegramUsername",
            "verified": False,
            "verification_date": "2020-01-01T00:00:00+03:00",
        },
    ],
}
APPLICANT_CREATE_REQUEST: Dict[str, Any] = {
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Michael",
    "money": "$100000",
    "phone": "89999999999",
    "email": "mail@some.domain.com",
    "skype": "my_skype",
    "position": "Front-end developer",
    "company": "Google Inc.",
    "photo": 1,
    "birthday": "2000-01-01",
    "externals": [
        {
            "auth_type": "NATIVE",
            "account_source": 5,
            "data": {"body": "Resume text"},
            "files": [1, 2, 3],
        },
    ],
    "social": [{"social_type": "TELEGRAM", "value": "TelegramUsername"}],
}
APPLICANT_CREATE_RESPONSE: Dict[str, Any] = {
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Michael",
    "money": "$100000",
    "phone": "89999999999",
    "email": "mail@some.domain.com",
    "skype": "my_skype",
    "position": "Front-end developer",
    "company": "Google Inc.",
    "photo": 1,
    "id": 19,
    "created": "2020-01-01T00:00:00+03:00",
    "birthday": "2020-01-01",
    "files": [1, 2, 3],
    "doubles": [{"double": 8}],
    "agreement": {"state": None, "decision_date": None},
    "external": [
        {
            "id": 1,
            "auth_type": "Auth",
            "account_source": 10,
            "updated": "2020-01-01T00:00:00+03:00",
        },
    ],
    "social": [
        {
            "id": 1,
            "social_type": "TELEGRAM",
            "value": "TelegramUsername",
            "verified": False,
            "verification_date": "2020-01-01T00:00:00+03:00",
        },
    ],
}
APPLICANT_PATCH_REQUEST: Dict[str, Any] = {"first_name": "Newname"}
APPLICANT_PATCH_RESPONSE: Dict[str, Any] = {
    "first_name": "Newname",
    "last_name": "Doe",
    "middle_name": "Michael",
    "money": "$100000",
    "phone": "89999999999",
    "email": "user@example.com",
    "skype": "my_skype",
    "position": "Front-end developer",
    "company": "Google Inc.",
    "photo": 1,
    "id": 1,
    "account": 5,
    "photo_url": "https://some.url/12341234",
    "birthday": "2020-01-01",
    "created": "2020-01-01T00:00:00+03:00",
    "tags": [{"tag": 1, "id": 1}],
    "links": [
        {
            "id": 7,
            "status": 12,
            "updated": "2020-01-01T00:00:00+03:00",
            "changed": "2020-01-01T00:00:00+03:00",
            "vacancy": 4,
        },
    ],
    "external": [
        {
            "id": 1,
            "auth_type": "Auth",
            "account_source": 10,
            "updated": "2020-01-01T00:00:00+03:00",
        },
    ],
    "agreement": {"state": None, "decision_date": None},
    "doubles": [{"double": 8}],
    "social": [
        {
            "id": 1,
            "social_type": "TELEGRAM",
            "value": "TelegramUsername",
            "verified": False,
            "verification_date": "2020-01-01T00:00:00+03:00",
        },
    ],
}

APPLICANT_SEARCH_BY_CURSOR_RESPONSE = {
    "items": [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "middle_name": "Michael",
            "birthday": "2020-01-01",
            "phone": "89999999999",
            "skype": "my_skype",
            "email": "user@example.com",
            "money": "$100000",
            "position": "Front-end developer",
            "company": "Google Inc.",
            "photo": 10,
            "photo_url": "https://hh.resume/12341234",
            "created": "2020-01-01T00:00:00+03:00",
        },
    ],
    "next_page_cursor": "3VudCI6IjoXIjogW10IiwgMy4wXX0=",
}


async def test_list_applicant(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants?count=30&page=1",
        json=APPLICANT_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    applicants = Applicant(api_client)

    response = await applicants.list(ACCOUNT_ID)
    assert response == ApplicantListResponse(**APPLICANT_LIST_RESPONSE)


async def test_get_applicant(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}",
        json=APPLICANT_GET_RESPONSE,
    )

    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    applicants = Applicant(api_client)

    response = await applicants.get(ACCOUNT_ID, APPLICANT_ID)
    assert response == ApplicantItem(**APPLICANT_GET_RESPONSE)


async def test_create_applicant(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants",
        json=APPLICANT_CREATE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = ApplicantCreateRequest(**APPLICANT_CREATE_REQUEST)
    applicants = Applicant(api_client)

    response = await applicants.create(ACCOUNT_ID, api_request)
    assert response == ApplicantCreateResponse(**APPLICANT_CREATE_RESPONSE)


async def test_patch_applicant(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}",
        json=APPLICANT_PATCH_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = ApplicantUpdateRequest(**APPLICANT_PATCH_REQUEST)
    applicants = Applicant(api_client)

    response = await applicants.patch(ACCOUNT_ID, APPLICANT_ID, api_request)
    assert response == ApplicantItem(**APPLICANT_PATCH_RESPONSE)


async def test_delete_applicant(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants" f"/{APPLICANT_ID}",
        status_code=204,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    applicants = Applicant(api_client)

    await applicants.delete(ACCOUNT_ID, APPLICANT_ID)


async def test_applicant_search_by_cursor(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/search_by_cursor?"
        "q=1&&status=1&&rejection_reason=1&&rejection_reason=2&&vacancy=null&&account_source=1"
        "&&only_current_status=false&&field=all&&count=30",
        status_code=200,
        json=APPLICANT_SEARCH_BY_CURSOR_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    applicants = Applicant(api_client)

    response = await applicants.search_by_cursor(
        ACCOUNT_ID,
        query="1",
        status=[1],
        rejection_reason=[1, 2],
        vacancy=[],
        account_source=[1],
    )
    assert response == ApplicantSearchByCursorResponse.model_validate(
        APPLICANT_SEARCH_BY_CURSOR_RESPONSE,
    )
    next_page_cursor = response.next_page_cursor
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/search_by_cursor?"
        f"next_page_cursor={next_page_cursor}",
        status_code=200,
        json=APPLICANT_SEARCH_BY_CURSOR_RESPONSE,
    )
    response = await applicants.search_by_cursor(ACCOUNT_ID, next_page_cursor=next_page_cursor)
    assert response == ApplicantSearchByCursorResponse.model_validate(
        APPLICANT_SEARCH_BY_CURSOR_RESPONSE,
    )
