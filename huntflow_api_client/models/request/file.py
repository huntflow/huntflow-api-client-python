from typing import Optional

from pydantic import ConfigDict, Field

from huntflow_api_client.models.common import RequestHeadersModel


class UploadFileHeaders(RequestHeadersModel):
    file_parse: Optional[bool] = Field(
        None,
        description="File will be processed by the system of field recognition",
        alias="x-file-parse",
    )
    ignore_lastname: Optional[str] = Field(
        None,
        description="Lastnames to ignore",
        alias="x-ignore-lastname",
    )
    ignore_email: Optional[str] = Field(
        None,
        description="Emails to ignore",
        alias="x-ignore-email",
    )
    ignore_phone: Optional[str] = Field(
        None,
        description="Phones to ignore",
        alias="x-ignore-phone",
    )

    model_config = ConfigDict(populate_by_name=True)
