from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin, ListEntityMixin
from huntflow_api_client.models.response.account_vacancy_request import (
    AccountVacancyRequestResponse,
    AccountVacancyRequestsListResponse,
)


class AccountVacancyRequest(BaseEntity, ListEntityMixin, GetEntityMixin):
    async def list(
        self,
        account_id: int,
        only_active: bool = True,
    ) -> AccountVacancyRequestsListResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/account_vacancy_requests
        :param account_id: Organization ID
        :param only_active: Show only active schemas flag, default = True

        :return: List of vacancy request schemas
        """
        path = f"/accounts/{account_id}/account_vacancy_requests"
        params = {
            "only_active": only_active,
        }
        response = await self._api.request("GET", path, params=params)
        return AccountVacancyRequestsListResponse.model_validate(response.json())

    async def get(
        self,
        account_id: int,
        account_vacancy_request_id: int,
    ) -> AccountVacancyRequestResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/account_vacancy_requests/-account_vacancy_request_id-
        :param account_id: Organization ID
        :param account_vacancy_request_id: Vacancy request schema ID

        :return: Specified vacancy request schema
        """
        path = f"/accounts/{account_id}/account_vacancy_requests/{account_vacancy_request_id}"
        response = await self._api.request("GET", path)
        return AccountVacancyRequestResponse.model_validate(response.json())
