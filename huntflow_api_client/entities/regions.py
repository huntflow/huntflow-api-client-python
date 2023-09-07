from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.response.regions import RegionsListResponse


class Region(BaseEntity, ListEntityMixin):
    async def list(self, account_id: int) -> RegionsListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/regions

        :param account_id: Organization ID
        :return: List of organization regions
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/regions")
        return RegionsListResponse.model_validate(response.json())
