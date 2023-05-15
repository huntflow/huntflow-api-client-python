import typing as t

from pydantic import BaseModel, Field, Extra, root_validator, PositiveInt

from huntflow_api_client.models.utils.fields import FieldType


class AccountVacancyRequestSchemaField(BaseModel):
    id: PositiveInt = Field(..., description="Field ID")
    type: FieldType = Field(..., description="Field type")
    title: t.Optional[str] = Field(None, description="Field title", example="Reason")
    required: bool = Field(False, description="Field required flag")
    order: int = Field(..., description="The order of the field on the form", example=1)
    values: t.Optional[t.List] = Field(
        None,
        description="List of possible values (for fields with `select` type)",
        example=["New position", "Replacing an employee"],
    )
    value: t.Optional[str] = Field(None, description="Default value", example="New position")
    fields: t.Optional[t.Dict[str, "AccountVacancyRequestSchemaField"]] = Field(
        None, description="Nested fields",
    )

    class Config:
        extra = Extra.allow


class AccountVacancyRequestSchema(BaseModel):
    _root_example = {
        "position": {
            "id": 130,
            "type": "string",
            "title": "Position",
            "required": True,
            "order": 1,
            "value": None,
            "pass_to_report": True,
            "account": 11,
            "key": "position",
        },
        "category": {
            "id": 132,
            "type": "dictionary",
            "title": "Category",
            "required": True,
            "order": 3,
            "value": None,
            "pass_to_report": True,
            "account": 11,
            "dictionary": "category",
            "vacancy_field": "category",
            "key": None,
        },
    }
    __root__: t.Dict[str, AccountVacancyRequestSchemaField] = Field(..., example=_root_example)

    @root_validator(pre=True)
    def prepare_data(cls, values: t.Dict) -> t.Dict[str, t.Dict[str, t.Any]]:
        return {"__root__": values}


class AccountVacancyRequestResponse(BaseModel):
    id: PositiveInt = Field(..., description="Schema ID", example=1)
    account: PositiveInt = Field(..., description="Organization ID", example=11)
    name: str = Field("", description="Schema name", example="IT Developers")
    attendee_required: t.Optional[bool] = Field(
        None,
        description=(
            "The flag of the presence of the 'Send for approval' "
            "field when creating an application "
            "(null - no field, false — optional field, true — required field)"
        ),
    )
    attendee_hint: str = Field(
        "", description="Hint under the field 'Send for approval'", example="Send for approval",
    )
    active: bool = Field(..., description="Schema activity flag")
    schema_: t.Optional[AccountVacancyRequestSchema] = Field(
        None, alias="schema", description="Description of schema fields",
    )


class AccountVacancyRequestsListResponse(BaseModel):
    items: list[AccountVacancyRequestResponse]
