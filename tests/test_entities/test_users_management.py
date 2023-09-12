from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.users_management import UsersManagement
from huntflow_api_client.models.consts import MemberType
from huntflow_api_client.models.request.users_management import ForeignUserRequest
from huntflow_api_client.models.response.users_management import (
    CreatedUserControlTaskResponse,
    ForeignUserResponse,
    ForeignUsersListResponse,
    UserControlTaskResponse,
    UserInternalIDResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
FOREIGN_USER_ID = "some_foreign_id"
TASK_ID = "073b8a60-4d8b-11ee-be56-0242ac120002"
GET_USERS_RESPONSE: Dict[str, Any] = {
    "page": 1,
    "count": 30,
    "total_pages": 2,
    "total_items": 50,
    "items": [
        {
            "id": FOREIGN_USER_ID,
            "name": "John Doe",
            "email": "mail@gmail.com",
            "type": "owner",
            "head_id": "user-032044",
            "division_ids": ["division-154", "division-871"],
            "permissions": ["string"],
            "meta": {},
        },
    ],
}
GET_USER_BY_FOREIGN_RESPONSE: Dict[str, Any] = {
    "id": FOREIGN_USER_ID,
    "name": "John Doe",
    "email": "mail@gmail.com",
    "type": "owner",
    "head_id": "user-032044",
    "division_ids": ["division-154", "division-871"],
    "permissions": ["string"],
    "meta": {},
}
GET_USER_CONTROL_TASK_RESPONSE: Dict[str, Any] = {
    "id": TASK_ID,
    "account_id": 0,
    "action": "CREATE",
    "status": "PENDING",
    "data": {},
    "comment": "string",
    "created": "2020-01-01T00:00:00+03:00",
    "completed": "2020-01-01T00:00:00+03:00",
}
GET_USER_ID_BY_FOREIGN_RESPONSE: Dict[str, Any] = {"id": 12345}
CREATE_USER_RESPONSE: Dict[str, Any] = {
    "task_id": TASK_ID,
    "action": "CREATE",
    "created": "2020-01-01T00:00:00+03:00",
}
UPDATE_USER_RESPONSE: Dict[str, Any] = {
    "task_id": TASK_ID,
    "action": "UPDATE",
    "created": "2020-01-01T00:00:00+03:00",
}


async def test_get_users_with_foreign(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/users/foreign?count=30&page=1",
        json=GET_USERS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    users_management = UsersManagement(api_client)

    response = await users_management.get_users_with_foreign(account_id=ACCOUNT_ID)
    assert response == ForeignUsersListResponse(**GET_USERS_RESPONSE)


async def test_get_user_by_foreign(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/users/foreign/{FOREIGN_USER_ID}",
        json=GET_USER_BY_FOREIGN_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    users_management = UsersManagement(api_client)

    response = await users_management.get_user_by_foreign(
        account_id=ACCOUNT_ID,
        foreign_user_id=FOREIGN_USER_ID,
    )
    assert response == ForeignUserResponse(**GET_USER_BY_FOREIGN_RESPONSE)


async def test_get_user_control_task(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/users/foreign/task/{TASK_ID}",
        json=GET_USER_CONTROL_TASK_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    users_management = UsersManagement(api_client)

    response = await users_management.get_user_control_task(account_id=ACCOUNT_ID, task_id=TASK_ID)
    assert response == UserControlTaskResponse(**GET_USER_CONTROL_TASK_RESPONSE)


async def test_get_user_internal_id_by_foreign(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/users/foreign/{FOREIGN_USER_ID}/id",
        json=GET_USER_ID_BY_FOREIGN_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    users_management = UsersManagement(api_client)

    response = await users_management.get_user_internal_id_by_foreign(
        account_id=ACCOUNT_ID,
        foreign_user_id=FOREIGN_USER_ID,
    )
    assert response == UserInternalIDResponse(**GET_USER_ID_BY_FOREIGN_RESPONSE)


async def test_delete_user(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/users/foreign/{FOREIGN_USER_ID}",
        status_code=204,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    users_management = UsersManagement(api_client)

    await users_management.delete_user(ACCOUNT_ID, FOREIGN_USER_ID)


async def test_create_user(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/users/foreign",
        json=CREATE_USER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    users_management = UsersManagement(api_client)
    data = ForeignUserRequest(
        id="some_id_12345",
        name="John",
        email="test@example.com",
        type=MemberType.owner,
    )
    response = await users_management.create_user(account_id=ACCOUNT_ID, data=data)
    assert response == CreatedUserControlTaskResponse(**CREATE_USER_RESPONSE)


async def test_update_user(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/users/foreign/{FOREIGN_USER_ID}",
        json=UPDATE_USER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    users_management = UsersManagement(api_client)
    data = ForeignUserRequest(
        id="some_id_12345",
        name="John",
        email="test@example.com",
        type=MemberType.owner,
    )
    response = await users_management.update_user(
        account_id=ACCOUNT_ID,
        foreign_user_id=FOREIGN_USER_ID,
        data=data,
    )
    assert response == CreatedUserControlTaskResponse(**UPDATE_USER_RESPONSE)
