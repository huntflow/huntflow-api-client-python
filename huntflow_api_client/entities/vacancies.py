from typing import Any, Dict, List, Optional, Union

from huntflow_api_client.entities.base import BaseEntity, CRUDEntityMixin
from huntflow_api_client.models.common import StatusResponse
from huntflow_api_client.models.request.vacancies import (
    VacancyCreateRequest,
    VacancyMemberCreateRequest,
    VacancyUpdatePartialRequest,
    VacancyUpdateRequest,
)
from huntflow_api_client.models.response.vacancies import (
    AdditionalFieldsSchemaResponse,
    LastVacancyFrameResponse,
    VacancyCreateResponse,
    VacancyFrameQuotasResponse,
    VacancyFramesListResponse,
    VacancyListResponse,
    VacancyQuotasResponse,
    VacancyResponse,
)


class Vacancy(BaseEntity, CRUDEntityMixin):
    async def get_additional_fields_schema(
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
            "GET",
            f"/accounts/{account_id}/vacancies/additional_fields",
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
            "GET",
            f"/accounts/{account_id}/vacancies",
            params=params,
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
            "POST",
            f"/accounts/{account_id}/vacancies",
            json=data.jsonable_dict(exclude_none=True),
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

    async def assign_coworker(
        self,
        account_id: int,
        vacancy_id: int,
        account_member_id: int,
        data: VacancyMemberCreateRequest,
    ) -> StatusResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/vacancies/-vacancy_id-/members/-account_member_id-

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param account_member_id: Coworker ID
        :param data: List of permissions
        :return: Status true or false
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/vacancies/{vacancy_id}/members/{account_member_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return StatusResponse(**response.json())

    async def remove_coworker(
        self,
        account_id: int,
        vacancy_id: int,
        account_member_id: int,
    ) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/vacancies/-vacancy_id-/members/-account_member_id-

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param account_member_id: Coworker ID
        """
        await self._api.request(
            "DELETE",
            f"/accounts/{account_id}/vacancies/{vacancy_id}/members/{account_member_id}",
        )

    async def get_frames(
        self,
        account_id: int,
        vacancy_id: int,
    ) -> VacancyFramesListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies/-vacancy_id-/frames

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :return: List of vacancy frames
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/vacancies/{vacancy_id}/frames",
        )
        return VacancyFramesListResponse(**response.json())

    async def get_last_frame(
        self,
        account_id: int,
        vacancy_id: int,
    ) -> LastVacancyFrameResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies/-vacancy_id-/frame

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :return: The last frame of a vacancy
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/vacancies/{vacancy_id}/frame",
        )
        return LastVacancyFrameResponse(**response.json())

    async def get_frame_quotas(
        self,
        account_id: int,
        vacancy_id: int,
        frame_id: int,
    ) -> VacancyFrameQuotasResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies/-vacancy_id-/frames/-frame_id-/quotas

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param frame_id: Vacancy frame ID
        :return: List of quotas for vacancy frame
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/vacancies/{vacancy_id}/frames/{frame_id}/quotas",
        )
        return VacancyFrameQuotasResponse(**response.json())

    async def get_quotas(
        self,
        account_id: int,
        vacancy_id: int,
        count: int = 30,
        page: int = 1,
    ) -> VacancyQuotasResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies/-vacancy_id-/quotas

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param count: Number of items per page
        :param page: Page number
        :return: Quotas for a vacancy
        """
        params: Dict[str, Any] = {"count": count, "page": page}
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/vacancies/{vacancy_id}/quotas",
            params=params,
        )
        return VacancyQuotasResponse.parse_obj(response.json())
