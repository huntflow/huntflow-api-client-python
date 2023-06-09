import json
from datetime import date, datetime
from typing import AbstractSet, Any, Callable, Dict, List, Mapping, Optional, Union

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.consts import (
    CalendarEventReminderMethod,
    EmailContactType,
    EventReminderMultiplier,
    VacancyState,
)

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


class JsonRequestModel(BaseModel):
    def jsonable_dict(
        self,
        *,
        include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        **dumps_kwargs: Any,
    ) -> Dict[str, Any]:
        params = {
            "include": include,
            "exclude": exclude,
            "by_alias": by_alias,
            "skip_defaults": skip_defaults,
            "exclude_unset": exclude_unset,
            "exclude_defaults": exclude_defaults,
            "exclude_none": exclude_none,
            "encoder": encoder,
        }
        return json.loads(self.json(**params, **dumps_kwargs))  # type: ignore


class PaginatedResponse(BaseModel):
    page: PositiveInt = Field(..., description="Page number", example=1)
    count: int = Field(..., description="Number of items per page", example=30)
    total_pages: int = Field(..., description="Total number of pages", example=2)


class Vacancy(BaseModel):
    account_division: Optional[PositiveInt] = Field(
        None,
        description="Division ID",
        example=12,
    )
    account_region: Optional[PositiveInt] = Field(
        None,
        description="Account region",
        example=1,
    )
    position: str = Field(
        ...,
        description="The name of the vacancy (occupation)",
        example="Developer",
    )
    company: Optional[str] = Field(
        None,
        description="Department (ignored if the DEPARTMENTS are enabled)",
        example="Google",
    )
    money: Optional[str] = Field(None, description="Salary", example="$10000")
    priority: Optional[int] = Field(
        None,
        description="The priority of a vacancy (0 for usual or 1 for high)",
        example=0,
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
        example=12,
    )


class EditedFillQuota(FillQuota):
    id: Optional[PositiveInt] = Field(None, description="Fill quota ID", example=15)


class File(BaseModel):
    id: PositiveInt = Field(..., description="File ID", example=19)
    url: AnyHttpUrl = Field(..., description="File URL")
    content_type: str = Field(..., description="MIME type of file", example="application/pdf")
    name: str = Field(..., description="File name", example="Resume.pdf")


class Applicant(BaseModel):
    first_name: Optional[str] = Field(None, description="First name", example="John")
    last_name: Optional[str] = Field(None, description="Last name", example="Doe")
    middle_name: Optional[str] = Field(None, description="Middle name", example="Michael")
    money: Optional[str] = Field(None, description="Salary expectation", example="$100000")
    phone: Optional[str] = Field(None, description="Phone number", example="89999999999")
    email: Union[EmailStr, str, None] = Field(
        None,
        description="Email address",
        example="mail@some.domain.com",
    )
    skype: Optional[str] = Field(None, description="Skype login", example="my_skype")
    position: Optional[str] = Field(
        None,
        description="Applicant’s occupation",
        example="Front-end developer",
    )
    company: Optional[str] = Field(
        None,
        description="Applicant’s place of work",
        example="Google Inc.",
    )
    photo: Optional[int] = Field(None, description="Applicant’s photo ID", example=1)


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
