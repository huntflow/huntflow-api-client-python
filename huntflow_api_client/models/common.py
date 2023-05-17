import json
from datetime import date, datetime
from typing import AbstractSet, Any, Callable, Dict, Mapping, Optional, Union

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.consts import EmailContactType, VacancyState

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
