from datetime import datetime
from typing import List

from pydantic import AnyHttpUrl, BaseModel, Field, PositiveInt

from huntflow_api_client.models.utils.common import WebhookEvent


class WebhookResponse(BaseModel):
    id: PositiveInt = Field(..., description="Webhook ID")
    account: PositiveInt = Field(..., description="Organization ID")
    url: AnyHttpUrl = Field(..., description="Webhook URL", example="https://example.com/hooks")
    created: datetime = Field(..., description="Date and time of creating a webhook")
    active: bool = Field(..., description="Webhook activity flag", example=True)
    webhook_events: List[WebhookEvent] = Field(..., description="Event types")


class WebhooksListResponse(BaseModel):
    items: List[WebhookResponse]
