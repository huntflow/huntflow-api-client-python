from typing import Any, Dict, List, Optional, Union

from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin, ListEntityMixin
from huntflow_api_client.models.consts import MemberType
from huntflow_api_client.models.response.coworkers import CoworkerResponse, CoworkersListResponse


class Coworker(BaseEntity, ListEntityMixin, GetEntityMixin):
    async def list(
        self,
        account_id: int,
        types: Optional[List[MemberType]] = None,
        fetch_permissions: Optional[bool] = None,
        vacancy_id: Optional[Union[int, List[int]]] = None,
        count: Optional[int] = 30,
        page: Optional[int] = 1,
    ) -> CoworkersListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/coworkers

        :param account_id: Organization ID
        :param types: Coworker types. Used to filter coworkers by their type (role).
            If not supplied, then coworkers of all types will be returned.
        :param fetch_permissions: Flag for returning coworker's permissions.
            If supplied, then all coworkers will contain a list of their permissions.
        :param vacancy_id: Vacancy ID or list of Vacancy ID
        :param count: Number of items per page
        :param page: Page number
        :return: List of coworkers with pagination
        """
        params: Dict[str, Any] = {
            "count": count,
            "page": page,
        }
        if types:
            params["type"] = [type_item.value for type_item in types]
        if fetch_permissions:
            params["fetch_permissions"] = fetch_permissions
        if vacancy_id:
            params["vacancy_id"] = vacancy_id
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/coworkers",
            params=params,
        )
        return CoworkersListResponse.model_validate(response.json())

    async def get(
        self,
        account_id: int,
        coworker_id: int,
        vacancy_id: Optional[int] = None,
    ) -> CoworkerResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/coworkers/-coworker_id-

        :param account_id: Organization ID
        :param coworker_id: Coworker ID
        :param vacancy_id: Vacancy ID
        :return: Specified coworker with a list of their permissions
        """
        params = {}
        if vacancy_id:
            params["vacancy_id"] = vacancy_id
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/coworkers",
            params=params,
        )
        return CoworkerResponse.model_validate(response.json())
