from typing import Union

from huntflow_api_client.entities.base import BaseEntity, CreateEntityMixin, UpdateEntityMixin
from huntflow_api_client.models.request.multi_vacancies import (
    MultiVacancyCreateRequest,
    MultiVacancyPartialUpdateRequest,
    MultiVacancyUpdateRequest,
)
from huntflow_api_client.models.response.muilti_vacancies import MultiVacancyResponse


class MultiVacancy(BaseEntity, CreateEntityMixin, UpdateEntityMixin):
    async def create(
        self,
        account_id: int,
        data: MultiVacancyCreateRequest,
    ) -> MultiVacancyResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/multi-vacancies

        :param account_id: Organization ID
        :param data: Data for creating multivacancy
        :return: Task ID
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/multi-vacancies",
            json=data.jsonable_dict(exclude_none=True),
        )
        return MultiVacancyResponse.model_validate(response.json())

    async def update(
        self,
        account_id: int,
        vacancy_id: int,
        data: Union[MultiVacancyUpdateRequest, MultiVacancyPartialUpdateRequest],
        partial: bool = False,
    ) -> MultiVacancyResponse:
        """
        API methods reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/multi-vacancies/-vacancy_id-
            https://api.huntflow.ai/v2/docs#patch-/accounts/-account_id-/multi-vacancies/-vacancy_id-

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param data: Data for updating multivacancy
        :param partial: Flag indicating that the multivacancy needs to be partially updated
        :return: Task ID
        """
        method = "PATCH" if partial else "PUT"
        response = await self._api.request(
            method,
            f"/accounts/{account_id}/multi-vacancies/{vacancy_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return MultiVacancyResponse.model_validate(response.json())
