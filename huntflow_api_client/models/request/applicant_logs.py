from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from huntflow_api_client.models.common import (
    ApplicantLogEmail,
    ApplicantLogIm,
    ApplicantLogSms,
    ApplicantOffer,
    CalendarEventAttendee,
    CalendarEventReminder,
    JsonRequestModel,
)
from huntflow_api_client.models.consts import CalendarEventType, Transparency


class ApplicantLogCalendarEvent(BaseModel):
    vacancy: Optional[PositiveInt] = Field(None, description="Vacancy ID")
    private: bool = Field(True, description="Event private flag")
    name: Optional[str] = Field(None, description="Event name")
    reminders: Optional[List[CalendarEventReminder]] = Field(None, description="List of reminders")
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


class CreateApplicantLogRequest(JsonRequestModel):
    comment: Optional[str] = Field(None, description="Comment text")
    vacancy: Optional[PositiveInt] = Field(
        None,
        description=(
            "Vacancy ID"
            "If this field is not set then the log will be added to `personal notes` block"
        ),
    )
    files: Optional[List[PositiveInt]] = Field(None, description="List of uploaded files ID")
    applicant_offer: Optional[ApplicantOffer] = Field(None, description="Applicant's offer")
    email: Optional[ApplicantLogEmail] = Field(None, description="Email object")
    calendar_event: Optional[ApplicantLogCalendarEvent] = Field(
        None,
        description="Calendar event object",
    )
    im: Optional[List[ApplicantLogIm]] = Field(None, max_length=1, description="Telegram message")
    sms: Optional[ApplicantLogSms] = Field(None, description="SMS message")
    survey_questionary_id: Optional[int] = Field(None, description="Survey questionary ID")

    model_config = ConfigDict(extra="allow")
