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
        path = f"/accounts/{account_id}"
        if coworker_id is not None:
            path += f"/coworkers/{coworker_id}"
        path += "/divisions"
        params = {"only_available": only_available}
        response = await self._api.request(
            "GET",
            path,
            params=params,
        )
        return DivisionsListResponse.parse_obj(response.json())

    async def create(
        self,
        account_id: int,
        divisions: BatchDivisionsRequest,
    ) -> BatchDivisionsResponse:
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/divisions/batch",
            json=divisions.jsonable_dict(exclude_none=True),
        )
        return BatchDivisionsResponse.parse_obj(response.json())
