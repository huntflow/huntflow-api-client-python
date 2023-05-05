from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    DeleteEntityMixin,
    ListEntityMixin,
)
from huntflow_api_client.models.request.webhooks import WebhookRequest
from huntflow_api_client.models.response.webhooks import WebhookResponse, WebhooksListResponse


class Webhook(BaseEntity, ListEntityMixin, CreateEntityMixin, DeleteEntityMixin):
    async def list(self, account_id: int) -> WebhooksListResponse:
        path = f"/accounts/{account_id}/hooks"
        response = await self._api.request("GET", path)
        return WebhooksListResponse(**response.json())

    async def create(self, account_id: int, data: WebhookRequest) -> WebhookResponse:
        path = f"/accounts/{account_id}/hooks"
        response = await self._api.request("POST", path, json=data.jsonable_dict(exclude_none=True))
        return WebhookResponse(**response.json())

    async def delete(self, account_id: int, webhook_id: int) -> None:
        path = f"/accounts/{account_id}/hooks/{webhook_id}"
        await self._api.request("DELETE", path)
