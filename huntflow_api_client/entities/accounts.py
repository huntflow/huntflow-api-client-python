from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin, ListEntityMixin
from huntflow_api_client.models.response.accounts import (
    MeResponse,
    OrganizationInfoResponse,
    OrganizationsListResponse,
)


class Account(BaseEntity, GetEntityMixin, ListEntityMixin):
    async def get_current_user(self) -> MeResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/me

        :return: Information about the current user
        """
        response = await self._api.request("GET", "/me")
        return MeResponse.model_validate(response.json())

    async def list(self) -> OrganizationsListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts

        :return: List of available organizations for the user
            associated with the passed authentication
        """
        response = await self._api.request("GET", "/accounts")
        return OrganizationsListResponse.model_validate(response.json())

    async def get(self, account_id: int) -> OrganizationInfoResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-

        :param account_id: Organization ID
        :return: Information about the specified organization
        """
        response = await self._api.request("GET", f"/accounts/{account_id}")
        return OrganizationInfoResponse.model_validate(response.json())
