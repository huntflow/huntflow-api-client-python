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
    async def list(  # noqa: A003
        self,
        account_id: int,
        vacancy_id: Optional[int] = None,
        count: int = 30,
        page: int = 1,
        values: bool = False,
    ) -> VacancyRequestListResponse:
        path = f"/accounts/{account_id}/vacancy_requests"
        params = {
            "count": count,
            "page": page,
            "values": values,
        }
        if vacancy_id:
            params["vacancy_id"] = vacancy_id

        response = await self._api.request("GET", path, params=params)
        return VacancyRequestListResponse.parse_obj(response.json())

    async def get(self, account_id: int, vacancy_request_id: int) -> VacancyRequestResponse:
        path = f"/accounts/{account_id}/vacancy_requests/{vacancy_request_id}"
        response = await self._api.request("GET", path)
        return VacancyRequestResponse.parse_obj(response.json())

    async def create(
        self,
        account_id: int,
        request_data: CreateVacancyRequestRequest,
    ) -> VacancyRequestResponse:
        path = f"/accounts/{account_id}/vacancy_requests"
        response = await self._api.request(
            "POST",
            path,
            json=request_data.jsonable_dict(exclude_none=True),
        )
        return VacancyRequestResponse.parse_obj(response.json())
