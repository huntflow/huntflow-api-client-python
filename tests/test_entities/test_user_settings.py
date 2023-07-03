from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.user_settings import UserSettings
from huntflow_api_client.models.response.user_settings import (
    CalendarAccountsListResponse,
    EmailAccountsListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

GET_USER_EMAIL_ACCOUNTS_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": 10,
            "name": "test@example.com",
            "email": "test@example.com",
            "receive": False,
            "send": False,
            "last_sync": "2020-01-01T00:00:00+03:00",
        },
    ],
}

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


async def test_get_email_accounts(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/email_accounts",
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
        url=f"{BASE_URL}/calendar_accounts",
        json=GET_USER_CALENDAR_ACCOUNTS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    settings = UserSettings(api_client)

    response = await settings.get_calendar_accounts()
    assert response == CalendarAccountsListResponse(**GET_USER_CALENDAR_ACCOUNTS_RESPONSE)
