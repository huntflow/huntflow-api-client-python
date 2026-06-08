from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.user_settings import UserSettings
from huntflow_api_client.models.common import StatusResponse
from huntflow_api_client.models.request.user_settings import (
    ExchangeEmailAccountRequest,
    OtherEmailAccountRequest,
)
from huntflow_api_client.models.response.user_settings import (
    CalendarAccountsListResponse,
    EmailAccount,
    EmailAccountsListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL, VERSIONED_BASE_URL

EMAIL_ACCOUNT: Dict[str, Any] = {
    "id": 10,
    "name": "test@example.com",
    "email": "test@example.com",
    "receive": False,
    "send": False,
    "last_sync": "2020-01-01T00:00:00+03:00",
}

GET_USER_EMAIL_ACCOUNTS_RESPONSE: Dict[str, Any] = {"items": [EMAIL_ACCOUNT]}

GET_USER_CALENDAR_ACCOUNTS_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": 10,
            "name": "john.smith@example.com",
            "auth_type": "AUTH_TYPE",
            "freebusy": False,
            "calendars": [
                {
                    "id": 1,
                    "foreign": "john.smith@example.com",
                    "name": "John Smith Personal Calendar",
                    "access_role": "owner",
                },
            ],
        },
    ],
}

EXCHANGE_EMAIL_ACCOUNT_CREATE_REQUEST: Dict[str, Any] = {
    "access_type": "DEFAULT",
    "email": "mail@mail.ru",
    "ews_url": "https://your-company.org/ews/exchange.asmx",
    "password": "string",
    "user": "string",
}

ACCOUNT_EMAIL_ID = 1

IMAP_EMAIL_ACCOUNT_CREATE_REQUEST: Dict[str, Any] = {
    "email": "mail@mail.ru",
    "password": "string",
    "inbound_host": "imap.your-company.org",
    "inbound_port": 1,
    "inbound_ssl": False,
    "outbound_host": "smtp.your-company.org",
    "outbound_port": 1,
    "outbound_ssl": False,
    "type": "IMAP",
}

DELETE_ACCOUNT_EMAIL_RESPONSE: Dict[str, Any] = {"status": True}


async def test_get_email_accounts(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/email_accounts",
        json=GET_USER_EMAIL_ACCOUNTS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    settings = UserSettings(api_client)

    response = await settings.get_email_accounts()
    assert response == EmailAccountsListResponse(**GET_USER_EMAIL_ACCOUNTS_RESPONSE)


async def test_get_calendar_accounts(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/calendar_accounts",
        json=GET_USER_CALENDAR_ACCOUNTS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    settings = UserSettings(api_client)

    response = await settings.get_calendar_accounts()
    assert response == CalendarAccountsListResponse(**GET_USER_CALENDAR_ACCOUNTS_RESPONSE)


async def test_create_exchange_email_account(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/email_accounts/exchange",
        json=EMAIL_ACCOUNT,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = ExchangeEmailAccountRequest(**EXCHANGE_EMAIL_ACCOUNT_CREATE_REQUEST)
    settings = UserSettings(api_client)

    response = await settings.create_exchange_email_account(api_request)
    assert response == EmailAccount(**EMAIL_ACCOUNT)


async def test_update_exchange_email_account(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/email_accounts/exchange/{ACCOUNT_EMAIL_ID}",
        json=EMAIL_ACCOUNT,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = ExchangeEmailAccountRequest(**EXCHANGE_EMAIL_ACCOUNT_CREATE_REQUEST)
    settings = UserSettings(api_client)

    response = await settings.update_exchange_email_account(api_request, ACCOUNT_EMAIL_ID)
    assert response == EmailAccount(**EMAIL_ACCOUNT)


async def test_create_other_email_account(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/email_accounts/other",
        json=EMAIL_ACCOUNT,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = OtherEmailAccountRequest(**IMAP_EMAIL_ACCOUNT_CREATE_REQUEST)
    settings = UserSettings(api_client)

    response = await settings.create_other_email_account(api_request)
    assert response == EmailAccount(**EMAIL_ACCOUNT)


async def test_update_other_email_account(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/email_accounts/other/{ACCOUNT_EMAIL_ID}",
        json=EMAIL_ACCOUNT,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)

    api_request = OtherEmailAccountRequest(**IMAP_EMAIL_ACCOUNT_CREATE_REQUEST)
    settings = UserSettings(api_client)

    response = await settings.update_other_email_account(api_request, ACCOUNT_EMAIL_ID)
    assert response == EmailAccount(**EMAIL_ACCOUNT)


async def test_delete_email_account(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/email_accounts/{ACCOUNT_EMAIL_ID}",
        json=DELETE_ACCOUNT_EMAIL_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    settings = UserSettings(api_client)

    response = await settings.delete_email_account(ACCOUNT_EMAIL_ID)
    assert response == StatusResponse(**DELETE_ACCOUNT_EMAIL_RESPONSE)
