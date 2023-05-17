from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.common import Applicant, EmailRecipient, JsonRequestModel
from huntflow_api_client.models.consts import (
    CalendarEventReminderMethod,
    CalendarEventType,
    EventReminderMultiplier,
    Transparency,
)


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


class ApplicantResumeUpdateData(BaseModel):
    body: Optional[str] = Field(..., description="Resume text")


class ApplicantResumeUpdateRequest(BaseModel):
    account_source: Optional[PositiveInt] = Field(..., description="Resume source ID")
    data: Optional[ApplicantResumeUpdateData] = Field(
        ...,
        description="Resume data",
    )
    files: Optional[List[PositiveInt]] = Field(
        [],
        max_items=1,
        description="Upload files<br>" "List of file's ID attached to the applicant resume",
    )


class ApplicantSocial(BaseModel):
    social_type: Literal["TELEGRAM"] = Field(..., description="Type")
    value: str = Field(..., description="Value")


class ApplicantCreateRequest(Applicant, JsonRequestModel):
    birthday: Optional[date] = Field(None, description="Date of birth")
    externals: Optional[List[ApplicantResumeCreate]] = Field(
        None,
        max_items=1,
        description="List of applicant's resumes",
    )
    social: List[ApplicantSocial] = Field(
        [],
        max_items=1,
        description="List of applicant's social accounts",
    )


class ApplicantUpdateRequest(Applicant, JsonRequestModel):
    birthday: Optional[date] = Field(None, description="Date of birth")
    social: Optional[List[ApplicantSocial]] = Field(
        None,
        max_items=1,
        description="List of applicant's social accounts",
    )


class CalendarEventReminder(BaseModel):
    multiplier: EventReminderMultiplier = Field(..., description="Reminder period")
    value: int = Field(..., gte=0, lt=40320, description="Reminder value")
    method: CalendarEventReminderMethod = Field(..., description="Reminder method")


class CalendarEventAttendee(BaseModel):
    member: Optional[PositiveInt] = Field(None, description="Coworker ID")
    name: Optional[str] = Field(None, description="Attendee name", alias="displayName")
    email: EmailStr = Field(..., description="Attendee email")

    class Config:
        allow_population_by_field_name = True


class EmailFollowup(BaseModel):
    id: PositiveInt = Field(..., description="Followup ID")
    account_member_template: int = Field(..., description="Email template ID")
    html: str = Field(..., description="Email content (HTML)")
    days: int = Field(
        ...,
        gte=1,
        description="The number of days after which to send a followup if there is no response",
    )


class ApplicantLogEmail(BaseModel):
    account_email: PositiveInt = Field(
        ...,
        description="Email account ID",
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="List of uploaded files ID",
    )
    followups: Optional[List[EmailFollowup]] = Field(
        None,
        description="List of email templates",
    )
    html: str = Field(..., description="Email content (HTML)")
    email: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    send_at: Optional[datetime] = Field(
        None,
        description="Date and time to send email. If not supplied, email will be sent immediately",
    )
    timezone: Optional[str] = Field(None, description="Time zone")
    to: Optional[List[EmailRecipient]] = Field(
        None,
        description="List of additional recipients (cc/bcc)",
    )
    reply: Optional[PositiveInt] = Field(None, description="Reply email ID")


class ApplicantLogIm(BaseModel):
    account_im: PositiveInt = Field(..., description="Account IM ID")
    receiver: str = Field(..., description="Username or phone of recipient")
    body: str = Field(..., description="Message text")


class ApplicantLogSms(BaseModel):
    phone: str = Field(..., description="Phone number of recipient")
    body: str = Field(..., description="Message text")


class ApplicantOffer(BaseModel):
    account_applicant_offer: PositiveInt = Field(..., description="Organization offer ID")
    values: dict = Field(..., description="Organization offer schema")


class ApplicantEvent(BaseModel):
    vacancy: Optional[PositiveInt] = Field(None, include_in_schema=False)
    private: bool = Field(True, description="Event private flag")
    name: Optional[str] = Field(None, description="Event name")
    reminders: Optional[List[CalendarEventReminder]] = Field(
        None,
        description="List of reminders <a href=https://tools.ietf.org/html/rfc5545>RFC 5545</a>",
    )
    location: Optional[str] = Field(None, max_length=1024, description="Event location")
    interview_type: Optional[PositiveInt] = Field(None, description="Interview type ID", example=17)
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
