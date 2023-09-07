from huntflow_api_client.entities.base import BaseEntity
from huntflow_api_client.models.response.user_settings import (
    CalendarAccountsListResponse,
    EmailAccountsListResponse,
)


class UserSettings(BaseEntity):
    async def get_email_accounts(self) -> EmailAccountsListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/email_accounts

        :return: List of user email accounts.
        """
        response = await self._api.request("GET", "/email_accounts")
        return EmailAccountsListResponse.model_validate(response.json())

    async def get_calendar_accounts(self) -> CalendarAccountsListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/calendar_accounts

        :return: List of user calendar accounts with associated calendars.
        """
        response = await self._api.request("GET", "/calendar_accounts")
        return CalendarAccountsListResponse.model_validate(response.json())
