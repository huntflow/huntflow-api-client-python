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
    attendees: t.Optional[t.List[VacancyRequestAttendee]] = Field(
        None,
        description="List of people to send a request for approval",
    )
    applicants_to_hire: t.Optional[int] = Field(
        None,
        le=999,
        gt=0,
        description="Number of applicants should be hired on the fill quota",
        include_in_schema=False,
    )
    files: t.Optional[t.List[PositiveInt]] = Field(
        None,
        description="List of file IDs to attach to the vacancy request.",
        example=[1, 2, 3],
    )

    class Config:
        extra = Extra.allow
