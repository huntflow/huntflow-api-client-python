from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin
from huntflow_api_client.models.response.users import UserResponse


class User(BaseEntity, GetEntityMixin):
    async def get(self, account_id: int, user_id: int) -> UserResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/users/-user_id-

        :param account_id: Organization ID
        :param user_id: User ID
        :return: The specified user with a list of his permissions
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/users/{user_id}")
        return UserResponse.model_validate(response.json())
