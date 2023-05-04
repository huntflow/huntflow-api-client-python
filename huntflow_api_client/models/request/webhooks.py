from typing import List

from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel


class WebhookRequest(JsonRequestModel):
    secret: str = Field(..., description="Secret key")
    url: str = Field(..., description="Webhook URL", example="https://example.com/hooks")
    active: bool = Field(..., description="Webhook activity flag", example=True)
    webhook_events: List[str] = Field(..., description="Events types")
