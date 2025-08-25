from typing import Optional

from pydantic import AnyHttpUrl, EmailStr, Field, PositiveInt

from huntflow_api_client.models.common import JsonRequestModel
from huntflow_api_client.models.consts import EmailInboundType, ExchangeAccessType


class ExchangeEmailAccountRequest(JsonRequestModel):
    """
    Model for EXCHANGE email connection
    """

    access_type: ExchangeAccessType = Field(..., description="Exchange access type")
    email: EmailStr = Field(..., description="Email address")
    ews_url: AnyHttpUrl = Field(..., description="Exchange server URL")
    password: str = Field(..., description="Exchange password")
    user: Optional[str] = Field(None, description="Exchange user name")


class OtherEmailAccountRequest(JsonRequestModel):
    """
    Model for IMAP/POP3 & SMTP email connection
    """

    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Mailbox password")

    inbound_host: str = Field(..., description="Inbound mail server URL without protocol")
    inbound_port: Optional[PositiveInt] = Field(None, description="Inbound mail port")
    inbound_ssl: bool = Field(False, description="Inbound mail server uses SSL")
    outbound_host: str = Field(..., description="Outbound mail server URL without protocol")
    outbound_port: Optional[PositiveInt] = Field(None, description="Outbound mail port")
    outbound_ssl: bool = Field(False, description="Outbound mail server uses SSL")
    type: EmailInboundType = Field(..., description="Type of inbound mail server")
