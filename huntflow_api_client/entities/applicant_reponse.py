from typing import Any, Dict

from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.response.applicant_response import ApplicantResponsesListResponse


class ApplicantResponse(BaseEntity, ListEntityMixin):
    async def list(
        self,
        account_id: int,
        applicant_id: int,
        count: int = 30,
        next_page_cursor: int = 1,
    ) -> ApplicantResponsesListResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2//docs#get-/accounts/-account_id-/applicants/-applicant_id-/responses

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param count: Number of items per page
        :param next_page_cursor: Next page cursor

        :return: List of applicant's worklog
        """
        path = f"/accounts/{account_id}/applicants/{applicant_id}/responses"
        params: Dict[str, Any] = {
            "count": count,
            "next_page_cursor": next_page_cursor,
        }

        response = await self._api.request("GET", path, params=params)
        return ApplicantResponsesListResponse.model_validate(response.json())
