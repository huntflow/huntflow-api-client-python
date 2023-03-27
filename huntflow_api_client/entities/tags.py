from huntflow_api_client.entities.base import BaseEntity, CRUDEntityMixin
from huntflow_api_client.models.request.tags import CreateAccountTagRequest
from huntflow_api_client.models.response.tags import AccountTagResponse


class AccountTag(BaseEntity, CRUDEntityMixin):
    async def get(self, account_id: int, account_tag_id: int) -> AccountTagResponse:
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/tags/{account_tag_id}",
        )
        return AccountTagResponse(**response.json())

    async def create(
        self,
        account_id: int,
        account_tag: CreateAccountTagRequest,
    ) -> AccountTagResponse:
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/tags",
            json=account_tag.jsonable_dict(),
        )
        return AccountTagResponse(**response.json())

    async def update(
        self,
        account_id: int,
        account_tag_id: int,
        data: CreateAccountTagRequest,
    ) -> AccountTagResponse:
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/tags/{account_tag_id}",
            json=data.jsonable_dict(),
        )
        return AccountTagResponse(**response.json())

    async def delete(self, account_id: int, account_tag_id: int) -> None:
        await self._api.request(
            "DELETE",
            f"/accounts/{account_id}/tags/{account_tag_id}",
        )
