from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.action_logs import ActionLog
from huntflow_api_client.models.response.action_logs import ActionLogsResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
ACTION_LOGS_LIST_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": 100,
            "user": {
                "id": 1,
                "name": "John Joe",
                "email": "user@example.com",
                "phone": "89999999999",
                "meta": {},
            },
            "log_type": "SUCCESS_LOGIN",
            "created": "2020-01-01T00:00:00+03:00",
            "action": "create",
            "ipv4": "127.0.0.1",
            "data": {},
        },
    ],
    "next_id": 70,
}


async def test_action_log_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/action_logs?count=30",
        json=ACTION_LOGS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    logs = ActionLog(api_client)

    response = await logs.list(ACCOUNT_ID)
    assert response == ActionLogsResponse(**ACTION_LOGS_LIST_RESPONSE)
