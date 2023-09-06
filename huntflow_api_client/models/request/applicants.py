from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, PositiveInt

from huntflow_api_client.models.common import (
    Applicant,
    CalendarEventAttendee,
    CalendarEventReminder,
    JsonRequestModel,
)
from huntflow_api_client.models.consts import CalendarEventType, Transparency


class ApplicantResumeData(BaseModel):
    body: Optional[str] = Field(None, description="Resume text")


class ApplicantResumeCreate(BaseModel):
    auth_type: Optional[str] = Field(None, description="Auth type")
    account_source: Optional[PositiveInt] = Field(None, description="Resume source ID")
    data: Optional[ApplicantResumeData] = Field(None, description="Resume data")
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="Upload files<br>" "List of file's ID attached to the applicant resume",
    )


class ApplicantSocial(BaseModel):
    social_type: Literal["TELEGRAM"] = Field(..., description="Type")
    value: str = Field(..., description="Value")


class ApplicantCreateRequest(Applicant, JsonRequestModel):
    birthday: Optional[date] = Field(None, description="Date of birth")
    externals: Optional[List[ApplicantResumeCreate]] = Field(
        None,
        max_length=1,
        description="List of applicant's resumes",
    )
    social: List[ApplicantSocial] = Field(
        [],
        max_length=1,
        description="List of applicant's social accounts",
    )


class ApplicantUpdateRequest(Applicant, JsonRequestModel):
    birthday: Optional[date] = Field(None, description="Date of birth")
    social: Optional[List[ApplicantSocial]] = Field(
        None,
        max_length=1,
        description="List of applicant's social accounts",
    )


class ApplicantEvent(BaseModel):
    vacancy: Optional[PositiveInt] = None
    private: bool = Field(True, description="Event private flag")
    name: Optional[str] = Field(None, description="Event name")
    reminders: Optional[List[CalendarEventReminder]] = Field(
        None,
        description="List of reminders <a href=https://tools.ietf.org/html/rfc5545>RFC 5545</a>",
    )
    location: Optional[str] = Field(None, max_length=1024, description="Event location")
    interview_type: Optional[PositiveInt] = Field(None, description="Interview type ID")
    event_type: CalendarEventType = Field(..., description="Calendar event type")
    description: Optional[str] = Field(None, description="Event description (comment)")
    calendar: PositiveInt = Field(..., description="Calendar ID")
    attendees: List[CalendarEventAttendee] = Field(
        ...,
        description="Event attendees (participants)",
    )
    start: datetime = Field(..., description="Event start date")
    end: datetime = Field(..., description="Event end date")
    timezone: Optional[str] = Field(None, description="Time zone")
    transparency: Transparency = Field(..., description="Event transparency (availability)")
