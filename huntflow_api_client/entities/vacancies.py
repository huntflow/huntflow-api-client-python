from typing import List, Union

from huntflow_api_client.entities.base import BaseEntity, CRUDEntityMixin, UpdateEntityMixin
from huntflow_api_client.models.request.vacancies import (
    VacancyCreateRequest,
    VacancyListState,
    VacancyUpdatePartialRequest,
    VacancyUpdateRequest,
)
from huntflow_api_client.models.response.vacancies import (
    AdditionalFieldsSchemaResponse,
    VacancyCreateResponse,
    VacancyListResponse,
    VacancyResponse,
)


class Vacancy(BaseEntity, CRUDEntityMixin, UpdateEntityMixin):
    async def get_org_vacancy_additional_fields_schema(
        self,
        account_id: int,
    ) -> AdditionalFieldsSchemaResponse:
        path = f"/accounts/{account_id}/vacancies/additional_fields"
        response = await self._api.request("GET", path)
        return AdditionalFieldsSchemaResponse(**response.json())

    async def list(  # noqa: A003
        self,
        account_id: int,
        count: int = 30,
        page: int = 1,
        mine: bool = False,
        state: Union[VacancyListState, List[VacancyListState]] = None,
    ) -> VacancyListResponse:
        params = {
            "count": count,
            "page": page,
            "mine": mine,
        }
        if state:
            params["state"] = state
        path = f"/accounts/{account_id}/vacancies"
        response = await self._api.request("GET", path, params=params)
        return VacancyListResponse(**response.json())

    async def get(self, account_id: int, vacancy_id: int) -> VacancyResponse:
        path = f"/accounts/{account_id}/vacancies/{vacancy_id}"
        response = await self._api.request("GET", path)
        return VacancyResponse(**response.json())

    async def create(self, account_id: int, data: VacancyCreateRequest) -> VacancyCreateResponse:
        path = f"/accounts/{account_id}/vacancies"
        response = await self._api.request("POST", path, json=data.jsonable_dict(exclude_none=True))
        return VacancyCreateResponse(**response.json())

    async def update(
        self,
        account_id: int,
        vacancy_id: int,
        data: VacancyUpdateRequest,
    ) -> VacancyResponse:
        path = f"/accounts/{account_id}/vacancies/{vacancy_id}"
        response = await self._api.request("PUT", path, json=data.jsonable_dict(exclude_none=True))
        return VacancyResponse(**response.json())

    async def delete(self, account_id: int, vacancy_id: int) -> None:
        path = f"/accounts/{account_id}/vacancies/{vacancy_id}"
        await self._api.request("DELETE", path)

    async def patch(
        self,
        account_id: int,
        vacancy_id: int,
        data: VacancyUpdatePartialRequest,
    ) -> VacancyResponse:
        path = f"/accounts/{account_id}/vacancies/{vacancy_id}"
        response = await self._api.request(
            "PATCH",
            path,
            json=data.jsonable_dict(exclude_none=True),
        )
        return VacancyResponse(**response.json())
