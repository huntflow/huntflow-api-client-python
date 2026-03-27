from typing import Dict, Optional, Union

from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.consts import RecommendationProcessingStatus
from huntflow_api_client.models.response.recommendation import RecommendationListResponse


class Recommendation(BaseEntity, ListEntityMixin):
    async def list(
        self,
        account_id: int,
        vacancy_id: int,
        count: int = 30,
        processing_status: RecommendationProcessingStatus = RecommendationProcessingStatus.ALL,
        next_page_cursor: Optional[str] = None,
    ) -> RecommendationListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/recommendations/-vacancy_id-

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param count: Number of items per page
        :param next_page_cursor: Next page cursor
        :param processing_status: Get all recommendations or processed/unprocessed only
        :return: A list of applicants recommended for a vacancy
        """
        params: Dict[str, Union[str, int]]
        if next_page_cursor is not None:
            params = {"next_page_cursor": next_page_cursor}
        else:
            params = {"count": count}
        params["processing_status"] = processing_status.value

        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/recommendations/{vacancy_id}",
            params=params,
        )
        return RecommendationListResponse.model_validate(response.json())
