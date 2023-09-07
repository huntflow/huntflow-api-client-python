from typing import Any, Dict, Optional

from huntflow_api_client.entities.base import BaseEntity
from huntflow_api_client.models.request.users_management import ForeignUserRequest
from huntflow_api_client.models.response.users_management import (
    CreatedUserControlTaskResponse,
    ForeignUserResponse,
    ForeignUsersListResponse,
    UserControlTaskResponse,
    UserInternalIDResponse,
)


class UsersManagement(BaseEntity):
    async def get_users_with_foreign(
        self,
        account_id: int,
        count: Optional[int] = 30,
        page: Optional[int] = 1,
    ) -> ForeignUsersListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/users/foreign

        :param account_id: Organization ID
        :param count: Number of items per page
        :param page: Page number

        :return: All users in organization with their permissions
            (vacancies permissions are not included),
            available divisions and their manager's identifiers.
            All identifiers in response are foreign.
        """
        params: Dict[str, Any] = {"count": count, "page": page}
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/users/foreign",
            params=params,
        )
        return ForeignUsersListResponse.model_validate(response.json())

    async def get_user_by_foreign(
        self,
        account_id: int,
        foreign_user_id: str,
    ) -> ForeignUserResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/users/foreign/-foreign_user_id-

        :param account_id: Organization ID
        :param foreign_user_id: Foreign ID of User

        :return: The specified user with his permissions, available divisions and his manager's
            identificators. All identifiers in request and response are foreign.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/users/foreign/{foreign_user_id}",
        )
        return ForeignUserResponse.model_validate(response.json())

    async def get_user_control_task(self, account_id: int, task_id: str) -> UserControlTaskResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/users/foreign/task/-task_id-

        :param account_id: Organization ID
        :param task_id: Task ID

        :return: Users management task handling result.
            All user identifiers in response are foreign.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/users/foreign/task/{task_id}",
        )
        return UserControlTaskResponse.model_validate(response.json())

    async def create_user(
        self,
        account_id: int,
        data: ForeignUserRequest,
    ) -> CreatedUserControlTaskResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/users/foreign

        :param account_id: Organization ID
        :param data: Data for creating a new user

        :return: Schedules a task to create a new user and returns the task's data.
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/users/foreign",
            content=data.model_dump_json(),
        )
        return CreatedUserControlTaskResponse.model_validate(response.json())

    async def delete_user(self, account_id: int, foreign_user_id: str) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/users/foreign/-foreign_user_id-

        :param account_id: Organization ID
        :param foreign_user_id: Foreign ID of User
        """
        await self._api.request(
            "DELETE",
            f"/accounts/{account_id}/users/foreign/{foreign_user_id}",
        )

    async def get_user_internal_id_by_foreign(
        self,
        account_id: int,
        foreign_user_id: str,
    ) -> UserInternalIDResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/users/foreign/-foreign_user_id-/id

        :param account_id: Organization ID
        :param foreign_user_id: Foreign ID of User

        :return: The internal ID of the specified user.
            Request user's identifier is foreign, response user's identifier is internal
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/users/foreign/{foreign_user_id}/id",
        )
        return UserInternalIDResponse.model_validate(response.json())

    async def update_user(
        self,
        account_id: int,
        foreign_user_id: str,
        data: ForeignUserRequest,
    ) -> CreatedUserControlTaskResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/users/foreign/-foreign_user_id-

        :param account_id: Organization ID
        :param foreign_user_id: Foreign ID of User
        :param data: Data for updating an existing user

        :return: Schedules a task to update existing user and returns the task's data.
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/users/foreign/{foreign_user_id}",
            content=data.model_dump_json(),
        )
        return CreatedUserControlTaskResponse.model_validate(response.json())
