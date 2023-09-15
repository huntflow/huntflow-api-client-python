import typing as t

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PositiveInt

from huntflow_api_client.models.common import JsonRequestModel


class VacancyRequestAttendee(BaseModel):
    email: EmailStr = Field(..., description="Attendee email")
    name: t.Optional[str] = Field(
        None,
        description="Attendee name",
    )


class CreateVacancyRequestRequest(JsonRequestModel):
    """
    The model accepts additional fields,
        which need to be specified for specified account vacancy request.

    Example:
        CreateVacancyRequestRequest(
            account_vacancy_request=1,
            position="my_position",
            my_field="my_value",
        )
    """

    account_vacancy_request: PositiveInt = Field(
        ...,
        description="Account vacancy request ID",
    )
    position: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The name of the vacancy (occupation)",
    )
    money: t.Optional[str] = Field(None, description="Salary")
    attendees: t.Optional[t.List[VacancyRequestAttendee]] = Field(
        None,
        description="List of people to send a request for approval",
    )
    files: t.Optional[t.List[PositiveInt]] = Field(
        None,
        description="List of file IDs to attach to the vacancy request.",
    )

    model_config = ConfigDict(extra="allow")
