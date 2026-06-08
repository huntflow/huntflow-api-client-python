from huntflow_api_client.entities.base import BaseEntity
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

    async def create_exchange_email_account(
        self,
        data: ExchangeEmailAccountRequest,
    ) -> EmailAccount:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/email_accounts/exchange

        :param data: Exchange user email account data
        :return: Created Exchange user email account for API robot.
        """
        response = await self._api.request(
            "POST",
            "/email_accounts/exchange",
            json=data.jsonable_dict(exclude_none=True),
        )
        return EmailAccount.model_validate(response.json())

    async def update_exchange_email_account(
        self,
        data: ExchangeEmailAccountRequest,
        account_email_id: int,
    ) -> EmailAccount:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/email_accounts/exchange/-account_email_id-

        :param account_email_id: Email account ID
        :param data: Exchange user email account data
        :return: Updated Exchange user email account for API robot.
        """
        response = await self._api.request(
            "PUT",
            f"/email_accounts/exchange/{account_email_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return EmailAccount.model_validate(response.json())

    async def create_other_email_account(
        self,
        data: OtherEmailAccountRequest,
    ) -> EmailAccount:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/email_accounts/other

        :param data: SMTP/POP3/IMAP user email account data
        :return: Created SMTP/POP3/IMAP user email account for API robot.
        """
        response = await self._api.request(
            "POST",
            "/email_accounts/other",
            json=data.jsonable_dict(exclude_none=True),
        )
        return EmailAccount.model_validate(response.json())

    async def update_other_email_account(
        self,
        data: OtherEmailAccountRequest,
        account_email_id: int,
    ) -> EmailAccount:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/email_accounts/other/-account_email_id-

        :param account_email_id: Email account ID
        :param data: SMTP/POP3/IMAP user email account data
        :return: Updated SMTP/POP3/IMAP user email account for API robot.
        """
        response = await self._api.request(
            "PUT",
            f"/email_accounts/other/{account_email_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return EmailAccount.model_validate(response.json())

    async def delete_email_account(self, account_email_id: int) -> StatusResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/email_accounts/-account_email_id-

        :param account_email_id: Email account ID
        """
        response = await self._api.request("DELETE", f"/email_accounts/{account_email_id}")
        return StatusResponse.model_validate(response.json())
