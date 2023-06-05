from typing import Any, Dict

from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel


class QuestionaryRequest(JsonRequestModel):
    """The successful response depends on the questionary schema."""

    __root__: Dict[str, Any] = Field(
        ...,
        description="Mapping of fields in the questionary and objects with their values",
    )
