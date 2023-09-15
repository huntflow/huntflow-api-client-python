import typing as t

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from huntflow_api_client.models.consts import FieldType


class AccountVacancyRequestSchemaField(BaseModel):
    id: PositiveInt = Field(..., description="Field ID")
    type: FieldType = Field(..., description="Field type")
    title: t.Optional[str] = Field(None, description="Field title")
    required: bool = Field(False, description="Field required flag")
    order: int = Field(..., description="The order of the field on the form")
    values: t.Optional[t.List] = Field(
        None,
        description="List of possible values (for fields with `select` type)",
    )
    value: t.Optional[str] = Field(None, description="Default value")
    fields: t.Optional[t.Dict[str, "AccountVacancyRequestSchemaField"]] = Field(
        None,
        description="Nested fields",
    )

    model_config = ConfigDict(extra="allow")


class AccountVacancyRequestResponse(BaseModel):
    id: PositiveInt = Field(..., description="Schema ID")
    account: PositiveInt = Field(..., description="Organization ID")
    name: str = Field("", description="Schema name")
    attendee_required: t.Optional[bool] = Field(
        None,
        description=(
            "The flag of the presence of the 'Send for approval' "
            "field when creating an application "
            "(null - no field, false — optional field, true — required field)"
        ),
    )
    attendee_hint: str = Field(
        "",
        description="Hint under the field 'Send for approval'",
    )
    active: bool = Field(..., description="Schema activity flag")
    schema_: t.Optional[t.Dict[str, AccountVacancyRequestSchemaField]] = Field(
        None,
        alias="schema",
        description="Description of schema fields",
    )


class AccountVacancyRequestsListResponse(BaseModel):
    items: t.List[AccountVacancyRequestResponse]
