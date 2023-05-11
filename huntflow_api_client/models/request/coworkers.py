from typing import List

from pydantic import Field, PositiveInt

from huntflow_api_client.models.common import JsonRequestModel


class PermissionItem(JsonRequestModel):
    permission: str = Field(..., description="Permission ID")
    value: PositiveInt = Field(..., description="Vacancy status ID")


class AssignCoworkerRequest(JsonRequestModel):
    permissions: List[PermissionItem]
