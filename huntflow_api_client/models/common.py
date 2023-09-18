import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Set, Union

import typing_extensions
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, EmailStr, Field, PositiveInt

from huntflow_api_client.models.consts import (
    CalendarEventReminderMethod,
    EmailContactType,
    EventReminderMultiplier,
    MemberType,
    VacancyState,
)

_FieldSet: typing_extensions.TypeAlias = "Set[int] | Set[str] | Dict[int, Any] | Dict[str, Any]"


class JsonRequestModel(BaseModel):
    def jsonable_dict(
        self,
        *,
        include: Optional[_FieldSet] = None,
        exclude: Optional[_FieldSet] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> Dict[str, Any]:
        return json.loads(
            self.model_dump_json(
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                round_trip=round_trip,
                warnings=warnings,
            ),
        )


class PaginatedResponse(BaseModel):
    page: PositiveInt = Field(..., description="Page number")
    count: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")


class Vacancy(BaseModel):
    account_division: Optional[PositiveInt] = Field(
        None,
        description="Division ID",
    )
    account_region: Optional[PositiveInt] = Field(
        None,
        description="Account region",
    )
    position: str = Field(
        ...,
        description="The name of the vacancy (occupation)",
    )
    company: Optional[str] = Field(
        None,
        description="Department (ignored if the DEPARTMENTS are enabled)",
    )
    money: Optional[str] = Field(None, description="Salary")
    priority: Optional[int] = Field(
        None,
        description="The priority of a vacancy (0 for usual or 1 for high)",
        ge=0,
        le=1,
    )
    hidden: bool = Field(False, description="Is the vacancy hidden from the colleagues?")
    state: VacancyState = Field(VacancyState.OPEN, description="The state of a vacancy")


class FillQuota(BaseModel):
    deadline: Optional[date] = Field(None, description="Date when the quota should be filled")
    applicants_to_hire: Optional[int] = Field(
        None,
        description="Number of applicants should be hired on the fill quota",
        ge=1,
        le=999,
    )
    vacancy_request: Optional[PositiveInt] = Field(
        None,
        description="Vacancy request ID",
    )


class EditedFillQuota(FillQuota):
    id: Optional[PositiveInt] = Field(None, description="Fill quota ID")


class File(BaseModel):
    id: PositiveInt = Field(..., description="File ID")
    url: AnyHttpUrl = Field(..., description="File URL")
    content_type: str = Field(..., description="MIME type of file")
    name: str = Field(..., description="File name")


class Applicant(BaseModel):
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    middle_name: Optional[str] = Field(None, description="Middle name")
    money: Optional[str] = Field(None, description="Salary expectation")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Union[EmailStr, str, None] = Field(
        None,
        description="Email address",
    )
    skype: Optional[str] = Field(None, description="Skype login")
    position: Optional[str] = Field(
        None,
        description="Applicant’s occupation",
    )
    company: Optional[str] = Field(
        None,
        description="Applicant’s place of work",
    )
    photo: Optional[int] = Field(None, description="Applicant’s photo ID")


class StatusResponse(BaseModel):
    status: bool = Field(True)


class VacancyQuotaBase(BaseModel):
    id: PositiveInt = Field(..., description="Fill quota ID")
    vacancy_frame: PositiveInt = Field(..., description="Vacancy frame ID")
    vacancy_request: Optional[PositiveInt] = Field(None, description="Vacancy request ID")
    created: datetime = Field(..., description="Date and time of creating a vacancy quota")
    changed: Optional[datetime] = Field(
        None,
        description="Date and time of updating a vacancy quota",
    )
    applicants_to_hire: PositiveInt = Field(
        ...,
        description="Number of applicants should be hired on the quota",
    )
    already_hired: int = Field(..., description="Number of applicants already hired on the quota")
    deadline: Optional[date] = Field(None, description="Date when the quota should be filled")
    closed: Optional[datetime] = Field(None, description="Date and time when the quota was closed")
    work_days_in_work: Optional[int] = Field(
        None,
        description="How many working days the vacancy is in work",
    )
    work_days_after_deadline: Optional[int] = Field(
        None,
        description="How many working days the vacancy is in work after deadline",
    )


class AccountInfo(BaseModel):
    id: PositiveInt = Field(..., description="ID of the user who opened the quota")
    name: str = Field(..., description="Name of the user who opened the quota")
    email: Optional[EmailStr] = Field(None, description="Email of the user who opened the quota")


class VacancyQuotaItem(VacancyQuotaBase):
    account_info: AccountInfo


class EmailRecipient(BaseModel):
    type: Optional[EmailContactType] = Field(None, description="Type of the email contact")
    name: Optional[str] = Field(
        None,
        description="Name of email recipient",
    )
    email: str = Field(..., description="Email address")


class EmailFollowup(BaseModel):
    id: PositiveInt = Field(..., description="Followup ID")
    account_member_template: int = Field(..., description="Email template ID")
    html: str = Field(..., description="Email content (HTML)")
    days: int = Field(
        ...,
        ge=1,
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


class CalendarEventReminder(BaseModel):
    multiplier: EventReminderMultiplier = Field(..., description="Reminder period")
    value: int = Field(..., ge=0, lt=40320, description="Reminder value")
    method: CalendarEventReminderMethod = Field(..., description="Reminder method")


class CalendarEventAttendee(BaseModel):
    member: Optional[PositiveInt] = Field(None, description="Coworker ID")
    name: Optional[str] = Field(None, description="Attendee name", alias="displayName")
    email: EmailStr = Field(..., description="Attendee email")

    model_config = ConfigDict(populate_by_name=True)


class SurveyQuestionaryRespondent(BaseModel):
    applicant_id: int = Field(..., description="Applicant ID")


class SurveyQuestionaryRespondentWithName(SurveyQuestionaryRespondent):
    name: str = Field(..., description="Applicant name")


class ForeignUser(BaseModel):
    id: str = Field(..., description="Foreign User ID")
    name: str = Field(..., description="User name")
    email: EmailStr = Field(..., description="Email")
    type: MemberType = Field(..., description="User type (role)")

    head_id: Optional[str] = Field(None, description="Foreign user ID of head")
    division_ids: Optional[List[str]] = Field(
        None,
        description="Foreign IDs of available divisions, case insensitive. "
        "If field is not provided, contains null or empty list, "
        "it means access to all divisions",
    )
    permissions: Optional[List[str]] = Field(
        None,
        description="User permissions. If field is not provided, "
        "contains null or empty list, it means no restrictions",
    )
    meta: Optional[Dict] = Field(None, description="Additional meta information")
