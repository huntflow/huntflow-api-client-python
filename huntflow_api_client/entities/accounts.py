from huntflow_api_client.entities.base import BaseEntity
from huntflow_api_client.models.response.accounts import (
    MeResponse,
    OrganizationInfoResponse,
    OrganizationsListResponse,
)


class Account(BaseEntity):
    async def get_current_user(self) -> MeResponse:
        """
        :return: Information about the current user
        """
        response = await self._api.request(
            "GET",
            "/me",
        )
        return MeResponse.parse_obj(response.json())

    async def available_org_list(self) -> OrganizationsListResponse:
        """
        :return: List of available organizations for the
        user associated with the passed authentication
        """
        response = await self._api.request(
            "GET",
            "/accounts",
        )
        return OrganizationsListResponse.parse_obj(response.json())

    async def get_org_info(self, account_id: int) -> OrganizationInfoResponse:
        """
        :param account_id: Organization ID
        :return: Information about the specified organization
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}",
        )
        return OrganizationInfoResponse.parse_obj(response.json())
