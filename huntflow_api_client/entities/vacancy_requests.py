from typing import Optional

from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    GetEntityMixin,
    ListEntityMixin,
)
from huntflow_api_client.models.request.vacancy_requests import CreateVacancyRequestRequest
from huntflow_api_client.models.response.vacancy_requests import (
    VacancyRequestListResponse,
    VacancyRequestResponse,
)


class VacancyRequest(BaseEntity, ListEntityMixin, GetEntityMixin, CreateEntityMixin):
    async def list(
        self,
        account_id: int,
        vacancy_id: Optional[int] = None,
        count: int = 30,
        page: int = 1,
        values: bool = False,
    ) -> VacancyRequestListResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancy_requests

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID. If supplied,
            only vacancy requests related to the specified vacancy will be returned
        :param count: Number of items per page
        :param page: Page number
        :param values: Show values flag. If True, vacancy requests fields will be included
        :return:  List of vacancy requests
        """
        path = f"/accounts/{account_id}/vacancy_requests"
        params = {
            "count": count,
            "page": page,
            "values": values,
        }
        if vacancy_id:
            params["vacancy_id"] = vacancy_id

        response = await self._api.request("GET", path, params=params)
        return VacancyRequestListResponse.model_validate(response.json())

    async def get(self, account_id: int, vacancy_request_id: int) -> VacancyRequestResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancy_requests/-vacancy_request_id-

        :param account_id: Organization ID
        :param vacancy_request_id: Vacancy request ID
        :return: Specified vacancy request's data
        """
        path = f"/accounts/{account_id}/vacancy_requests/{vacancy_request_id}"
        response = await self._api.request("GET", path)
        return VacancyRequestResponse.model_validate(response.json())

    async def create(
        self,
        account_id: int,
        request_data: CreateVacancyRequestRequest,
    ) -> VacancyRequestResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/vacancy_requests

        :param account_id: Organization ID
        :param request_data: Request body structure
        :return: Created vacancy request's data
        """
        path = f"/accounts/{account_id}/vacancy_requests"
        response = await self._api.request(
            "POST",
            path,
            json=request_data.jsonable_dict(exclude_none=True),
        )
        return VacancyRequestResponse.model_validate(response.json())
