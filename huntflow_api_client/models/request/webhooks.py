from typing import List

from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel
from huntflow_api_client.models.consts import WebhookEvent


class WebhookRequest(JsonRequestModel):
    secret: str = Field(..., description="Secret key")
    url: str = Field(..., description="Webhook URL")
    active: bool = Field(..., description="Webhook activity flag")
    webhook_events: List[WebhookEvent] = Field(..., description="List of webhook events")
