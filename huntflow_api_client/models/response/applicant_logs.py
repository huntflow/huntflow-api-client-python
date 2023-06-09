from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from huntflow_api_client.models.common import (
    ApplicantLogAccountInfo,
    ApplicantLogCalendarEvent,
    ApplicantLogEmailResponse,
    ApplicantLogSurveyQuestionary,
    File,
    PaginatedResponse,
    VacancyQuotaItem,
)
from huntflow_api_client.models.consts import ApplicantLogType, CalendarEventReminderMethod
from huntflow_api_client.models.response.applicant_offers import ApplicantVacancyOffer


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


class ApplicantOffer(BaseModel):
    id: int = Field(..., description="Applicant's offer ID")
    account_applicant_offer: int = Field(..., description="Organization's offer ID")
    created: datetime = Field(..., description="Date and time of creating an offer")


class CreateApplicantLogResponse(BaseModel):
    id: int = Field(..., description="Log ID")
    applicant: int = Field(..., description="Applicant ID")
    type: ApplicantLogType = Field(..., description="Log type")
    vacancy_id: Optional[int] = Field(None, alias="vacancy", description="Vacancy ID")
    status: Optional[int] = Field(None, description="Vacancy status ID")
    rejection_reason: Optional[int] = Field(None, description="Rejection reason ID")
    created: datetime = Field(..., description="Date and time of creation of the log")
    employment_date: Optional[date] = Field(None, description="Employment date")
    applicant_offer: Optional[ApplicantOffer] = Field(..., description="Offer object")
    comment: Optional[str] = Field(None, description="Comment text", example="Example comment")
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

    class Config:
        extra = Extra.allow
        allow_population_by_field_name = True
