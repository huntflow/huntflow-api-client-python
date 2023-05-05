from typing import List

from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel
from huntflow_api_client.models.utils.common import WebhookEvent


class WebhookRequest(JsonRequestModel):
    secret: str = Field(..., description="Secret key")
    url: str = Field(..., description="Webhook URL", example="https://example.com/hooks")
    active: bool = Field(..., description="Webhook activity flag", example=True)
    webhook_events: List[WebhookEvent] = Field(..., description="List of webhook events")
