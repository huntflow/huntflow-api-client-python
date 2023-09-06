from typing import Optional

from huntflow_api_client.entities.base import BaseEntity, CreateEntityMixin, ListEntityMixin
from huntflow_api_client.models.request.divisions import BatchDivisionsRequest
from huntflow_api_client.models.response.divisions import (
    BatchDivisionsResponse,
    DivisionsListResponse,
)


class AccountDivision(BaseEntity, ListEntityMixin, CreateEntityMixin):
    async def list(
        self,
        account_id: int,
        coworker_id: Optional[int] = None,
        only_available: bool = False,
    ) -> DivisionsListResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/divisions
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/coworkers/-coworker_id-/divisions

        :param account_id: Organization ID
        :param coworker_id: If specified - will be returned divisions for specified coworker
        :param only_available:	If True,
            then only divisions available to the current user will be returned

        :raises ValueError:
            Only one parameter from `coworker_id` and `only_available` must be specified

        :return: List of company divisions.
        """
        if coworker_id is not None and only_available:
            raise ValueError(
                "Only one parameter from coworker_id and only_available must be specified",
            )
        path = f"/accounts/{account_id}"
        if coworker_id is not None:
            path += f"/coworkers/{coworker_id}"
            params = {}
        else:
            params = {"only_available": only_available}
        path += "/divisions"
        response = await self._api.request(
            "GET",
            path,
            params=params,
        )
        return DivisionsListResponse.model_validate(response.json())

    async def create(
        self,
        account_id: int,
        divisions: BatchDivisionsRequest,
    ) -> BatchDivisionsResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/divisions/batch

        :param account_id: Organization ID
        :param divisions: Request body structure

        :return: An object that contains the task ID of the background update task
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/divisions/batch",
            json=divisions.jsonable_dict(exclude_none=True),
        )
        return BatchDivisionsResponse.model_validate(response.json())
