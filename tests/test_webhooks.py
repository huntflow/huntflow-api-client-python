from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.webhooks import Webhook
from huntflow_api_client.models.consts import WebhookEvent
from huntflow_api_client.models.request.webhooks import WebhookRequest
from huntflow_api_client.models.response.webhooks import WebhookResponse, WebhooksListResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
HOOK_ID = 2

WEBHOOK_LIST_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": HOOK_ID,
            "account": ACCOUNT_ID,
            "url": "https://some.site/hook/handler",
            "created": "2023-05-04T17:21:14+03:00",
            "active": True,
            "webhook_events": ["APPLICANT"],
        },
    ],
}

WEBHOOK_CREATE_RESPONSE: Dict[str, Any] = {
    "id": HOOK_ID,
    "account": ACCOUNT_ID,
    "url": "https://some.site/hook/handler",
    "created": "2023-05-04T17:24:28+03:00",
    "active": True,
    "webhook_events": ["APPLICANT"],
}


async def test_list_webhooks(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/hooks",
        json=WEBHOOK_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    webhooks = Webhook(api_client)

    response = await webhooks.list(ACCOUNT_ID)
    assert response == WebhooksListResponse(**WEBHOOK_LIST_RESPONSE)


async def test_create_webhook(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/hooks",
        json=WEBHOOK_CREATE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    webhooks = Webhook(api_client)

    data = WebhookRequest(
        secret="",
        url="https://some.site/hook/handler",
        active=True,
        webhook_events=[WebhookEvent.APPLICANT, WebhookEvent.VACANCY],
    )
    response = await webhooks.create(ACCOUNT_ID, data)
    assert response == WebhookResponse(**WEBHOOK_CREATE_RESPONSE)


async def test_delete_webhook(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/hooks/{HOOK_ID}",
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    webhooks = Webhook(api_client)

    await webhooks.delete(ACCOUNT_ID, HOOK_ID)
