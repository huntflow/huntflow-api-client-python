from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.response.rejection_reason import RejectionReasonsListResponse


class RejectionReason(BaseEntity, ListEntityMixin):
    async def list(self, account_id: int) -> RejectionReasonsListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/rejection_reasons

        :param account_id: Organization ID
        :return: List of applicant on vacancy rejection reasons
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/rejection_reasons")
        return RejectionReasonsListResponse.model_validate(response.json())
