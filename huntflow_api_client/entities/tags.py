from huntflow_api_client.entities.base import BaseEntity
from huntflow_api_client.models.request.tags import CreateAccountTagRequest
from huntflow_api_client.models.response.tags import AccountTagResponse


class AccountTag(BaseEntity):
    async def get(self, account_id: int, account_tag_id: int) -> AccountTagResponse:
        async with self.client as client:
            response = await client.get(f"/v2/accounts/{account_id}/tags/{account_tag_id}")
        return AccountTagResponse(**response.json())

    async def create(
        self, account_id: int, account_tag: CreateAccountTagRequest,
    ) -> AccountTagResponse:
        async with self.client as client:
            response = await client.post(
                f"/v2/accounts/{account_id}/tags", json=account_tag.jsonable_dict()
            )
        return AccountTagResponse(**response.json())

    async def update(
        self,
        account_id: int,
        account_tag_id: int,
        data: CreateAccountTagRequest
    ) -> AccountTagResponse:
        async with self.client as client:
            response = await client.put(
                f"/v2/accounts/{account_id}/tags/{account_tag_id}", json=data.jsonable_dict(),
            )
        return AccountTagResponse(**response.json())

    async def delete(self, account_id: int, account_tag_id: int) -> None:
        async with self.client as client:
            await client.delete(f"/v2/accounts/{account_id}/tags/{account_tag_id}")
