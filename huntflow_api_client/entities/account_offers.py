from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin, ListEntityMixin
from huntflow_api_client.models.response.account_offers import (
    AccountOfferResponse,
    AccountOffersListResponse,
)


class AccountOffer(BaseEntity, GetEntityMixin, ListEntityMixin):
    async def list(self, account_id: int) -> AccountOffersListResponse:
        """
        API method reference: https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/offers

        :param account_id: Organization ID

        :return: List of organization's offers
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/offers")
        return AccountOffersListResponse.model_validate(response.json())

    async def get(self, account_id: int, offer_id: int) -> AccountOfferResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/offers/-offer_id-

        :param account_id: Organization ID
        :param offer_id: Offer ID

        :return: Organization's offer with a schema of values
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/offers/{offer_id}")
        return AccountOfferResponse.model_validate(response.json())
