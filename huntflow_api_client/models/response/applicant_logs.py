from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from huntflow_api_client.models.common import (
    ApplicantOffer,
    CalendarEventAttendee,
    File,
    PaginatedResponse,
    VacancyQuotaItem,
)
from huntflow_api_client.models.consts import (
    ApplicantLogType,
    CalendarEventReminderMethod,
    CalendarEventStatus,
    CalendarEventType,
    EmailContactType,
    SurveyType,
    Transparency,
)
from huntflow_api_client.models.response.applicant_offers import ApplicantVacancyOffer


class BaseSurveySchemaType(BaseModel):
    id: int = Field(..., description="Survey ID")
    name: str = Field(..., description="Survey name")
    type: SurveyType = Field(..., description="Survey type")
    active: bool = Field(..., description="Is survey active?")
    created: datetime = Field(..., description="Date and time of creating a survey")
    updated: datetime = Field(..., description="Date and time of the last update of the survey")


class SurveySchemaTypeQLogResponse(BaseSurveySchemaType):
    title: Optional[str] = Field(..., description="Survey title")


class ApplicantLogSurveyQuestionary(BaseModel):
    id: int = Field(..., description="Survey questionary ID")
    survey: SurveySchemaTypeQLogResponse = Field(..., description="Survey schema")
    survey_answer_id: Optional[int] = Field(
        None,
        description="Survey questionary answer ID",
    )
    created: datetime = Field(
        ...,
        description="Date and time of creating an survey questionary",
    )


class EmailRecipient(BaseModel):
    type: Optional[EmailContactType] = Field(None, description="Type of the email contact")
    name: Optional[str] = Field(
        None,
        description="Name of email recipient",
    )
    email: str = Field(..., description="Email address")


class ApplicantLogAccountInfo(BaseModel):
    id: int = Field(..., description="ID of the user who created the log")
    name: str = Field(..., description="Name of the user who created the log")


class CalendarEventCreator(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Event creator name",
    )
    email: str = Field(..., description="Event creator email")
    self: Optional[bool] = Field(
        False,
        description="Flag indicating that you are the creator of the event",
    )


class CalendarEventReminderResponse(BaseModel):
    method: CalendarEventReminderMethod = Field(
        ...,
        description="Reminder method",
    )
    minutes: int = Field(..., description="How many minutes in advance to remind about the event")


class ApplicantLogCalendarEvent(BaseModel):
    id: PositiveInt = Field(..., description="Calendar event ID")
    name: Optional[str] = Field(
        None,
        description="Event name",
    )
    all_day: bool = Field(
        ...,
        description="Flag indicating that the event is scheduled for the whole day",
    )
    created: datetime = Field(..., description="Date and time of event creation")
    creator: Optional[CalendarEventCreator] = Field(None, description="Event creator")
    description: Optional[str] = Field(
        None,
        description="Event description",
    )
    timezone: Optional[str] = Field(None, description="Event time zone")
    start: datetime = Field(..., description="Event start date and time")
    end: datetime = Field(..., description="Event end date and time")
    etag: Optional[str] = Field(None, description="Event Etag")
    event_type: CalendarEventType = Field(..., description="Event type")
    interview_type: Optional[int] = Field(None, description="Interview type ID")
    calendar: PositiveInt = Field(..., description="Calendar ID")
    vacancy: Optional[PositiveInt] = Field(
        None,
        description="Vacancy ID",
    )
    foreign: Optional[str] = Field(None, description="Foreign ID of event")
    location: Optional[str] = Field(None, description="Event location")
    attendees: List[CalendarEventAttendee] = Field(
        [],
        description="Event attendees (participants)",
    )
    reminders: List[CalendarEventReminderResponse] = Field(
        [],
        description="List of reminders <a href=https://tools.ietf.org/html/rfc5545>RFC 5545</a>",
    )
    status: CalendarEventStatus = Field(..., description="Event status")
    transparency: Transparency = Field(..., description="Event transparency (availability)")
    recurrence: Optional[List] = None


class ApplicantLogEmailResponse(BaseModel):
    id: int = Field(..., description="Email ID")
    created: datetime = Field(..., description="Date and time of creating email")
    subject: Optional[str] = Field(None, description="Email subject")
    email_thread: Optional[int] = Field(None, description="Email thread ID")
    account_email: Optional[int] = Field(None, description="Email account ID")
    files: Optional[List[File]] = Field(None, description="List of uploaded files ID")
    foreign: Optional[str] = Field(None, description="Foreign email ID")
    timezone: str = Field(..., description="Time zone")
    html: Optional[str] = Field(None, description="Email content (HTML)")
    from_email: Optional[str] = Field(None, description="Sender email address")
    from_name: Optional[str] = Field(None, description="Sender name")
    replyto: Optional[List[str]] = Field(
        None,
        description="List of email foreign IDs, to which a reply is send",
    )
    send_at: Optional[datetime] = Field(None, description="Date and time to send email")
    to: Optional[List[EmailRecipient]] = Field(None, description="Recipients list")
    state: Optional[str] = Field(None, description="Email state")


class ApplicantLogItem(BaseModel):
    id: int = Field(..., description="Log ID")
    type: Optional[ApplicantLogType] = Field(None, description="Log type")
    vacancy: Optional[int] = Field(None, description="Vacancy ID")
    status: Optional[int] = Field(None, description="Vacancy status ID")
    source: Optional[str] = Field(None, description="Source ID")
    rejection_reason: Optional[int] = Field(None, description="Rejection reason ID")
    created: datetime = Field(..., description="Date and time of creation of the log")
    employment_date: Optional[date] = Field(None, description="Employment date")
    account_info: ApplicantLogAccountInfo = Field(..., description="The user who created the log")
    comment: Optional[str] = Field(None, description="Comment text")
    files: List[File] = Field([], description="List of files attached to the log")
    calendar_event: Optional[ApplicantLogCalendarEvent] = Field(None, description="Calendar event")
    hired_in_fill_quota: Optional[VacancyQuotaItem] = Field(
        None,
        description="Quota data by which applicant was hired",
    )
    applicant_offer: Optional[ApplicantVacancyOffer] = Field(None, description="Applicant's offer")
    email: Optional[ApplicantLogEmailResponse] = Field(None, description="Email object")
    survey_questionary: Optional[ApplicantLogSurveyQuestionary] = Field(
        None,
        description="Survey questionary",
    )


class ApplicantLogResponse(PaginatedResponse):
    items: List[ApplicantLogItem] = Field(..., description="List of applicant's logs")


class CreateApplicantLogResponse(BaseModel):
    id: int = Field(..., description="Log ID")
    applicant: int = Field(..., description="Applicant ID")
    type: ApplicantLogType = Field(..., description="Log type")
    vacancy: Optional[int] = Field(None, description="Vacancy ID")
    status: Optional[int] = Field(None, description="Vacancy status ID")
    rejection_reason: Optional[int] = Field(None, description="Rejection reason ID")
    created: datetime = Field(..., description="Date and time of creation of the log")
    employment_date: Optional[date] = Field(None, description="Employment date")
    applicant_offer: Optional[ApplicantOffer] = Field(..., description="Offer object")
    comment: Optional[str] = Field(None, description="Comment text")
    files: List[File] = Field([], description="List of files attached to the log")
    calendar_event: Optional[ApplicantLogCalendarEvent] = Field(
        None,
        description="Calendar event object",
    )
    email: Optional[ApplicantLogEmailResponse] = Field(None, description="Email object")
    survey_questionary: Optional[ApplicantLogSurveyQuestionary] = Field(
        None,
        description="Survey Questionary",
    )

    model_config = ConfigDict(extra="allow")
