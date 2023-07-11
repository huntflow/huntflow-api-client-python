from typing import List, Optional, Union

from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel


class UploadFileHeaders(JsonRequestModel):
    file_parse: Optional[bool] = Field(
        None,
        description="File will be processed by the system of field recognition",
        alias="x-file-parse",
    )
    ignore_lastname: Optional[Union[str, List[str]]] = Field(
        None,
        description="Lastname",
        alias="x-ignore-lastname",
    )
    ignore_email: Optional[Union[str, List[str]]] = Field(
        None,
        description="Email",
        alias="x-ignore-email",
    )
    ignore_phone: Optional[Union[str, List[str]]] = Field(
        None,
        description="Phone",
        alias="x-ignore-phone",
    )
