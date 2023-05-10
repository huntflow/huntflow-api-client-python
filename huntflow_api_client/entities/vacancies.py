from typing import Any, Dict, List, Optional, Union

from huntflow_api_client.entities.base import BaseEntity, CRUDEntityMixin, UpdateEntityMixin
from huntflow_api_client.models.request.vacancies import (
    VacancyCreateRequest,
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
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies/additional_fields

        :param account_id: Organization ID
        :return: Schema of additional fields for vacancies set in organization
        """
        response = await self._api.request(
            "GET", f"/accounts/{account_id}/vacancies/additional_fields",
        )
        return AdditionalFieldsSchemaResponse(**response.json())

    async def list(
        self,
        account_id: int,
        count: int = 30,
        page: int = 1,
        mine: bool = False,
        state: Optional[Union[str, List[str]]] = None,
    ) -> VacancyListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies

        :param account_id: Organization ID
        :param count: Number of items per page
        :param page: Page number
        :param mine: Shows only vacancies that the current user is working on
        :param state: The state of a vacancy
        :return:  List of vacancies
        """
        params: Dict[str, Any] = {
            "count": count,
            "page": page,
            "mine": mine,
        }
        if state:
            params["state"] = state
        response = await self._api.request(
            "GET", f"/accounts/{account_id}/vacancies", params=params,
        )
        return VacancyListResponse(**response.json())

    async def get(self, account_id: int, vacancy_id: int) -> VacancyResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies/-vacancy_id-

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :return: The specified vacancy
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/vacancies/{vacancy_id}")
        return VacancyResponse(**response.json())

    async def create(self, account_id: int, data: VacancyCreateRequest) -> VacancyCreateResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/vacancies

        :param account_id: Organization ID
        :param data: Vacancy data
        :return: The created vacancy
        """
        response = await self._api.request(
            "POST", f"/accounts/{account_id}/vacancies", json=data.jsonable_dict(exclude_none=True),
        )
        return VacancyCreateResponse(**response.json())

    async def update(
        self,
        account_id: int,
        vacancy_id: int,
        data: VacancyUpdateRequest,
    ) -> VacancyResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/vacancies/-vacancy_id-

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param data: Vacancy data
        :return: The updated vacancy
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/vacancies/{vacancy_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return VacancyResponse(**response.json())

    async def delete(self, account_id: int, vacancy_id: int) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/vacancies/-vacancy_id-

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        """
        await self._api.request("DELETE", f"/accounts/{account_id}/vacancies/{vacancy_id}")

    async def patch(
        self,
        account_id: int,
        vacancy_id: int,
        data: VacancyUpdatePartialRequest,
    ) -> VacancyResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#patch-/accounts/-account_id-/vacancies/-vacancy_id-

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param data: Vacancy data
        :return: The updated vacancy
        """
        response = await self._api.request(
            "PATCH",
            f"/accounts/{account_id}/vacancies/{vacancy_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return VacancyResponse(**response.json())
