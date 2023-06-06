from datetime import date, datetime
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.common import Applicant, File, PaginatedResponse, VacancyQuotaItem
from huntflow_api_client.models.consts import AgreementState as AgreementStateEnum
from huntflow_api_client.models.consts import (
    ApplicantLogType,
    CalendarEventReminderMethod,
    CalendarEventStatus,
    CalendarEventType,
    EmailContactType,
    Transparency,
)
from huntflow_api_client.models.response.offers import ApplicantVacancyOffer
from huntflow_api_client.models.response.survey import SurveySchemaTypeQLogResponse


class ApplicantTag(BaseModel):
    tag: int = Field(..., description="Tag ID")
    id: int = Field(..., description="Applicant's tag ID")


class ApplicantLink(BaseModel):
    id: Optional[int] = Field(None, description="Link ID")
    status: int = Field(..., description="Vacancy status ID")
    updated: datetime = Field(
        ...,
        description="The date of the applicant's update at a vacancy",
    )
    changed: datetime = Field(
        ...,
        description="The date of the latest changes at the current recruitment stage",
    )
    vacancy_id: int = Field(..., alias="vacancy", description="Vacancy ID")

    class Config:
        allow_population_by_field_name = True


class ApplicantResume(BaseModel):
    id: int = Field(..., description="Resume ID")
    auth_type: Optional[str] = Field(None, description="The format of resume")
    account_source: Optional[int] = Field(None, description="Resume source ID")
    updated: Optional[datetime] = Field(
        None,
        description="The date and time of resume update",
    )


class ApplicantAgreement(BaseModel):
    state: Optional[AgreementStateEnum] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
    )
    decision_date: Optional[datetime] = Field(
        None,
        description="Date of applicant's decision to personal data processing",
    )


class ApplicantDouble(BaseModel):
    double: int = Field(..., description="The ID of a duplicated applicant")


class ApplicantSocial(BaseModel):
    id: PositiveInt = Field(..., description="Social ID")
    social_type: str = Field(..., description="Type")
    value: str = Field(..., description="Value")
    verified: bool = Field(..., description="Verification flag")
    verification_date: Optional[datetime] = Field(None, description="Verification date")


class ApplicantItem(Applicant):
    id: int = Field(..., description="Applicant ID")
    account: int = Field(..., description="Organization ID")
    photo_url: Optional[str] = Field(
        None,
        description="A link to an applicant’s photo",
    )
    birthday: Optional[date] = Field(None, description="Date of birth")
    created: Optional[datetime] = Field(
        ...,
        description="Date and time of adding an applicant",
    )
    email: Union[EmailStr, str, None] = Field(
        None,
        description="Email address",
    )
    tags: List[ApplicantTag] = Field(..., description="List of tags")
    links: List[ApplicantLink] = Field(..., description="Applicant's vacancies")
    external: Optional[List[ApplicantResume]] = Field(None, description="Applicant's resume")
    agreement: Optional[ApplicantAgreement] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
    )
    doubles: List[ApplicantDouble] = Field(..., description="List of duplicates")
    social: List[ApplicantSocial] = Field(..., description="List of applicant's social accounts")


class ApplicantListResponse(PaginatedResponse):
    total_items: Optional[int] = Field(..., description="Total number of items")
    items: List[ApplicantItem] = Field(..., description="List of applicants")


class ApplicantCreateResponse(Applicant):
    id: int = Field(..., description="Applicant ID")
    created: datetime = Field(
        ...,
        description="Date and time of adding an applicant",
    )
    birthday: Optional[date] = Field(None, description="Date of birth")
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="Upload files<br>The list of file's ID attached to the applicant",
    )
    doubles: List[ApplicantDouble] = Field(..., description="List of duplicates")
    agreement: Optional[ApplicantAgreement] = Field(
        None,
        description="Agreement's state of applicant to personal data processing",
    )
    external: List[ApplicantResume] = Field(..., description="Applicant's resume")
    social: List[ApplicantSocial] = Field(..., description="List of applicant's social accounts")


class ApplicantSearchItem(BaseModel):
    id: int = Field(..., description="Applicant ID")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    middle_name: Optional[str] = Field(None, description="Middle name")
    birthday: Optional[date] = Field(None, description="Date of birth")
    phone: Optional[str] = Field(None, description="Phone number")
    skype: Optional[str] = Field(None, description="Skype login")
    email: Union[EmailStr, str, None] = Field(None, description="Email address")
    money: Optional[str] = Field(None, description="Salary expectation")
    position: Optional[str] = Field(None, description="Candidate’s occupation")
    company: Optional[str] = Field(None, description="Candidate’s place of work")
    photo: Optional[int] = Field(None, description="Candidate’s photo ID")
    photo_url: Optional[str] = Field(None, description="A link to a candidate’s photo")
    created: datetime = Field(..., description="Date and time of adding a candidate")


class ApplicantSearchByCursorResponse(BaseModel):
    items: List[ApplicantSearchItem] = Field(..., description="List of applicants")
    next_page_cursor: Optional[str] = Field(None, description="Next page cursor")


class EmailRecipient(BaseModel):
    type: Optional[EmailContactType] = Field(None, description="Type of the email contact")
    name: Optional[str] = Field(
        None,
        description="Name of email recipient",
    )
    email: str = Field(..., description="Email address")


class ApplicantLogEmailResponse(BaseModel):
    id: int = Field(..., description="Email ID")
    created: datetime = Field(
        ...,
        description="Date and time of creating email",
    )
    subject: Optional[str] = Field(None, description="Email subject")
    email_thread: Optional[int] = Field(None, description="Email thread ID")
    account_email: Optional[int] = Field(
        None,
        description="Email account ID",
    )
    files: Optional[List[File]] = Field(None, description="List of uploaded files ID")
    foreign: Optional[str] = Field(None, description="Foreign email ID")
    timezone: str = Field(
        ...,
        description="Time zone",
    )
    html: Optional[str] = Field(
        None,
        description="Email content (HTML)",
    )
    from_email: Optional[str] = Field(
        None,
        description="Sender email address",
    )
    from_name: Optional[str] = Field(
        None,
        description="Sender name",
    )
    replyto: Optional[List[str]] = Field(
        None,
        description="List of email foreign IDs, to which a reply is send",
    )
    send_at: Optional[datetime] = Field(
        None,
        description="Date and time to send email",
    )
    to: Optional[List[EmailRecipient]] = Field(None, description="Recipients list")
    state: Optional[str] = Field(None, description="Email state")


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


class CalendarEventAttendee(BaseModel):
    member: Optional[int] = Field(None, description="Coworker ID")
    name: Optional[str] = Field(
        None,
        description="Attendee name",
    )
    email: str = Field(
        ...,
        description="Attendee email",
    )
    status: Optional[CalendarEventStatus] = Field(
        None,
        description="Attendee response status",
    )


class CalendarEventReminder(BaseModel):
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
        example="Interview with John Doe",
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
    reminders: List[CalendarEventReminder] = Field(
        [],
        description="List of reminders <a href=https://tools.ietf.org/html/rfc5545>RFC 5545</a>",
    )
    status: CalendarEventStatus = Field(..., description="Event status")
    transparency: Transparency = Field(..., description="Event transparency (availability)")
    recurrence: Optional[List] = None


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


class ApplicantLogItem(BaseModel):
    id: int = Field(..., description="Log ID")
    type: Optional[ApplicantLogType] = Field(
        None,
        description="Log type",
    )
    vacancy_id: Optional[int] = Field(
        None,
        alias="vacancy",
        description="Vacancy ID",
    )
    status: Optional[int] = Field(
        None,
        description="Vacancy status ID",
    )
    source: Optional[str] = Field(None, description="Source ID")
    rejection_reason: Optional[int] = Field(
        None,
        description="Rejection reason ID",
    )
    created: datetime = Field(
        ...,
        description="Date and time of creation of the log",
    )
    employment_date: Optional[date] = Field(None, description="Employment date")
    account_info: ApplicantLogAccountInfo = Field(..., description="The user who created the log")
    comment: Optional[str] = Field(None, description="Comment text")
    files: List[File] = Field([], description="List of files attached to the log")
    calendar_event: Optional[ApplicantLogCalendarEvent] = Field(
        None,
        description="Calendar event",
    )
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
