from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import DelayedTask
from huntflow_api_client.models.response.delayed_tasks import DelayedTaskResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

DELAYED_TASKS_RESPONSE = {
    "task_id": "1882e199-a310-4000-8706-490f0822fa01",
    "state": "enqueued",
    "created": 1561006501.318867,
    "updated": 1561006501.318867,
    "created_datetime": "2020-01-01T00:00:00+03:00",
    "updated_datetime": "2020-01-01T00:00:00+03:00",
    "states_log": [
        {
            "state": "enqueued",
            "timestamp": 1561006501.318867,
            "datetime": "2020-01-01T00:00:00+03:00",
            "comment": "Some text",
        },
    ],
}


ACCOUNT_ID = 1
TASK_ID = "1"


async def test_get_delayed_task(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/delayed_tasks/{TASK_ID}",
        json=DELAYED_TASKS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    tasks = DelayedTask(api_client)
    response = await tasks.get(ACCOUNT_ID, TASK_ID)
    assert response == DelayedTaskResponse.model_validate(DELAYED_TASKS_RESPONSE)
