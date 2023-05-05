from huntflow_api_client.entities.base import BaseEntity
from huntflow_api_client.models.response.accounts import (
    MeResponse,
    OrganizationInfoResponse,
    OrganizationsListResponse,
)


class Account(BaseEntity):
    async def get_current_user(self) -> MeResponse:
        path = "/me"
        response = await self._api.request(
            "GET",
            path,
        )
        return MeResponse.parse_obj(response.json())

    async def available_org_list(self) -> OrganizationsListResponse:
        path = "/accounts"
        response = await self._api.request(
            "GET",
            path,
        )
        return OrganizationsListResponse.parse_obj(response.json())

    async def get_org_info(self, account_id: int) -> OrganizationInfoResponse:
        path = f"/accounts/{account_id}"
        response = await self._api.request(
            "GET",
            path,
        )
        return OrganizationInfoResponse.parse_obj(response.json())
