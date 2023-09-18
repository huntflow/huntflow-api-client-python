import typing as t

from pydantic import BaseModel, ConfigDict, Field, RootModel

from huntflow_api_client.models.consts import FieldType


class QuestionaryField(BaseModel):
    type: FieldType = Field(..., description="Field type")
    id: int = Field(..., description="Field ID")
    title: t.Optional[str] = Field(None, description="Field title")
    required: bool = Field(False, description="Field required flag")
    order: int = Field(..., description="The order of the field on the form")
    values: t.Optional[t.List] = Field(
        None,
        description="List of possible values (for fields with select type)",
    )
    value: t.Optional[str] = Field(None, description="Set value")
    fields_: t.Optional[t.Dict[str, "QuestionaryField"]] = Field(
        None,
        description="Child fields",
        alias="fields",
    )
    show_in_profile: t.Optional[bool] = Field(
        None,
        description="Display field value in applicant's profile",
    )
    dictionary: t.Optional[str] = Field(
        None,
        description="Organization dictionary name (for type=dictionary)",
    )

    model_config = ConfigDict(extra="allow")


class QuestionarySchemaResponse(RootModel):
    root: t.Dict[str, QuestionaryField] = Field(
        ...,
        description="Mapping of fields in the questionary and objects with their values",
    )
