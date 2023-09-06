from datetime import date
from typing import List, Optional

from pydantic import Field, PositiveInt

from huntflow_api_client.models.common import (
    ApplicantLogEmail,
    ApplicantLogIm,
    ApplicantLogSms,
    ApplicantOffer,
    JsonRequestModel,
)
from huntflow_api_client.models.request.applicants import ApplicantEvent


class AddApplicantToVacancyRequest(JsonRequestModel):
    vacancy: PositiveInt = Field(..., description="Vacancy ID")
    status: PositiveInt = Field(..., description="Vacancy status ID")
    comment: Optional[str] = Field(None, description="Comment text")
    rejection_reason: Optional[PositiveInt] = Field(
        None,
        description="Rejection reason ID.The reason of the rejection (if the status is 'rejected')",
    )
    fill_quota: Optional[PositiveInt] = Field(
        None,
        description="Fill quota ID (if the status is 'hired')",
    )
    employment_date: Optional[date] = Field(
        None,
        description="Employment date (if the status is 'hired')",
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        max_length=15,
        description="Upload files. The list of file's ID attached to the log",
    )
    calendar_event: Optional[ApplicantEvent] = Field(None, description="Calendar event object")
    email: Optional[ApplicantLogEmail] = Field(None, description="Email object")
    im: Optional[List[ApplicantLogIm]] = Field(None, max_length=1, description="Telegram message")
    sms: Optional[ApplicantLogSms] = Field(None, description="SMS message")
    applicant_offer: Optional[ApplicantOffer] = Field(None, description="Applicant's offer")
    survey_questionary_id: Optional[int] = Field(None, description="Survey questionary ID")


class ChangeVacancyApplicantStatusRequest(JsonRequestModel):
    vacancy: PositiveInt = Field(..., description="Vacancy ID")
    status: PositiveInt = Field(..., description="Vacancy status ID")
    comment: Optional[str] = Field(None, description="Comment text")
    rejection_reason: Optional[PositiveInt] = Field(
        None,
        description="Rejection reason ID.The reason of the rejection (if the status is 'rejected')",
    )
    fill_quota: Optional[PositiveInt] = Field(
        None,
        description="Fill quota ID (if the status is 'hired')",
    )
    employment_date: Optional[date] = Field(
        None,
        description="Employment date (if the status is 'hired')",
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        max_length=15,
        description="Upload files. The list of file's ID attached to the log",
    )
    applicant_offer: Optional[ApplicantOffer] = Field(None, description="Applicant's offer")
    calendar_event: Optional[ApplicantEvent] = Field(None, description="Calendar event object")
    email: Optional[ApplicantLogEmail] = Field(None, description="Email object")
    im: Optional[List[ApplicantLogIm]] = Field(None, max_length=1, description="Telegram message")
    sms: Optional[ApplicantLogSms] = Field(None, description="SMS message")
    survey_questionary_id: Optional[int] = Field(None, description="Survey questionary ID")


class ApplicantVacancySplitRequest(JsonRequestModel):
    applicant: int = Field(..., description="Applicant ID")
    status: int = Field(..., description="Account vacancy status ID")
    fill_quota: Optional[int] = Field(None, description="Fill quota ID for hiring")
    employment_date: Optional[date] = Field(None, description="Employment date")
    rejection_reason: Optional[int] = Field(
        None,
        description="Rejection reason ID for trash status",
    )
