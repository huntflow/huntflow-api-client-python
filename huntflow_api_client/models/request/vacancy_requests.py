import typing as t

from pydantic import BaseModel, EmailStr, Extra, Field, PositiveInt

from huntflow_api_client.models.common import JsonRequestModel


class VacancyRequestAttendee(BaseModel):
    email: EmailStr = Field(..., description="Attendee email")
    name: t.Optional[str] = Field(
        None,
        description="Attendee name",
        example="John Doe",
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
        example=1,
    )
    position: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The name of the vacancy (occupation)",
        example="Developer",
    )
    money: t.Optional[str] = Field(None, description="Salary", example="$10000")
    attendees: t.Optional[list[VacancyRequestAttendee]] = Field(
        None,
        description="List of people to send a request for approval",
    )
    files: t.Optional[list[PositiveInt]] = Field(
        None,
        description="List of file IDs to attach to the vacancy request.",
        example=[1, 2, 3],
    )

    class Config:
        extra = Extra.allow
