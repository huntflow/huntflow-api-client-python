import typing as t

from pydantic import BaseModel, EmailStr, Extra, Field, PositiveInt, conint, constr

from huntflow_api_client.models.common import JsonRequestModel


class VacancyRequestAttendee(BaseModel):
    email: EmailStr = Field(..., description="Attendee email")
    name: t.Optional[str] = Field(
        None,
        description="Attendee name",
        example="John Doe",
    )


class CreateVacancyRequestRequest(JsonRequestModel):
    account_vacancy_request: PositiveInt = Field(
        ...,
        description="Account vacancy request ID",
        example=1,
    )
    position: constr(min_length=1, max_length=255) = Field(
        ...,
        description="The name of the vacancy (occupation)",
        example="Developer",
    )
    money: t.Optional[str] = Field(None, description="Salary", example="$10000")
    attendees: t.Optional[list[VacancyRequestAttendee]] = Field(
        None, description="List of people to send a request for approval",
    )
    applicants_to_hire: t.Optional[conint(gt=0, le=999)] = Field(
        None,
        description="Number of applicants should be hired on the fill quota",
        include_in_schema=False,
    )
    files: t.Optional[list[PositiveInt]] = Field(
        None,
        description="List of file IDs to attach to the vacancy request.",
        example=[1, 2, 3],
    )

    class Config:
        extra = Extra.allow
