from huntflow_api_client.entities.base import BaseEntity, CRUDEntityMixin
from huntflow_api_client.models.request.tags import CreateAccountTagRequest
from huntflow_api_client.models.response.tags import AccountTagResponse


class AccountTag(BaseEntity, CRUDEntityMixin):
    async def get(self, account_id: int, account_tag_id: int) -> AccountTagResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/tags/-tag_id-

        :param account_id: Organization ID
        :param account_tag_id: Tag ID
        :return: The specified tag
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/tags/{account_tag_id}")
        return AccountTagResponse(**response.json())

    async def create(
        self,
        account_id: int,
        account_tag: CreateAccountTagRequest,
    ) -> AccountTagResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/tags

        :param account_id: Organization ID
        :param account_tag: Tag data
        :return: Tag
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/tags",
            json=account_tag.jsonable_dict(exclude_none=True),
        )
        return AccountTagResponse(**response.json())

    async def update(
        self,
        account_id: int,
        account_tag_id: int,
        data: CreateAccountTagRequest,
    ) -> AccountTagResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/tags/-tag_id-

        :param account_id: Organization ID
        :param account_tag_id: Tag ID
        :param data: Tag data
        :return: Tag
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/tags/{account_tag_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return AccountTagResponse(**response.json())

    async def delete(self, account_id: int, account_tag_id: int) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/hooks/-webhook_id-

        :param account_id: Organization ID
        :param account_tag_id: Tag ID
        """
        await self._api.request(
            "DELETE",
            f"/accounts/{account_id}/tags/{account_tag_id}",
        )
