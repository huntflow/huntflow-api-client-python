import typing as t
from datetime import date, datetime

from pydantic import BaseModel, Field, PositiveInt, EmailStr

from huntflow_api_client_python.serializers.common import AgreementState, Applicant


class ApplicantTag(BaseModel):
    tag: int = Field(..., description="Tag ID", example=1)
    id: int = Field(..., description="Applicant tag ID", example=1)


class ApplicantLink(BaseModel):
    id: t.Optional[int] = Field(None, description="Link ID", example=7)
    status: int = Field(..., description="Vacancy status ID", example=12)
    updated: datetime = Field(
        ..., description="The date of the applicant's update at a vacancy",
    )
    changed: datetime = Field(
        ..., description="The date of the latest changes at the current recruitment stage",
    )
    vacancy_id: int = Field(
        ..., alias="vacancy", description="Vacancy ID", example=4
    )

    class Config:
        allow_population_by_field_name = True


class ApplicantResume(BaseModel):
    id: int = Field(..., description="Resume ID", example=1)
    auth_type: str = Field(None, description="The format of resume", example="HH")
    account_source: int = Field(None, description="Applicant source ID", example=10)
    updated: datetime = Field(
        None, description="The date and time of resume update",
    )


class ApplicantAgreement(BaseModel):
    state: AgreementState = Field(
        None, description="Agreement state", example=AgreementState.accepted
    )
    decision_date: datetime = Field(
        None, description="Date of applicant's decision to personal data processing",
    )


class ApplicantDouble(BaseModel):
    double: int = Field(..., description="The ID of a duplicated applicant", example=8)


class ApplicantSocial(BaseModel):
    id: PositiveInt = Field(..., description="Social ID", example=1)
    social_type: str = Field(..., description="Type", example="TELEGRAM")
    value: str = Field(..., description="Value", example="TelegramUsername")
    verified: bool = Field(..., description="Verification flag")
    verification_date: t.Optional[datetime] = Field(None, description="Verification date")


class ApplicantItem(Applicant):
    id: int = Field(..., description="Applicant ID", example=1)
    account: int = Field(..., description="Organization ID", example=5)
    photo_url: str = Field(
        None, description="A link to an applicant’s photo", example="https://hh.resume/12341234",
    )
    birthday: date = Field(None, description="Date of birth", example="2020-01-01")
    created: datetime = Field(
        ..., description="Date and time of adding an applicant",
    )
    email: t.Union[EmailStr, str] = Field(None, description="Email address", example="mail@mail.ru")
    tags: t.List[ApplicantTag] = Field(..., description="List of tags")
    links: t.List[ApplicantLink] = Field(..., description="Applicant's vacancies")
    external: t.Optional[t.List[ApplicantResume]] = Field(None, description="Applicant's resume")
    agreement: ApplicantAgreement = Field(
        None, description="Agreement state", example=AgreementState.declined
    )
    doubles: t.List[ApplicantDouble] = Field(..., description="List of duplicates")
    social: t.List[ApplicantSocial] = Field(..., description="List of applicant's social accounts")


class ApplicantUpdateResponse(ApplicantItem):
    pass


class ApplicantCreateResponse(Applicant):
    id: int = Field(..., description="Applicant ID", example=19)
    created: datetime = Field(
        ..., description="Date and time of adding an applicant",
    )
    birthday: date = Field(None, description="Date of birth", example="2020-01-01")
    files: t.List[PositiveInt] = Field(
        None,
        description="The list of file's ID attached to the applicant",
        example=[1, 2, 3],
    )
    doubles: t.List[ApplicantDouble] = Field(..., description="List of duplicates")
    agreement: ApplicantAgreement = Field(
        None, description="Agreement state", example=AgreementState.sent
    )
    external: t.List[ApplicantResume] = Field(..., description="Applicant's resume")
    social: t.List[ApplicantSocial] = Field(..., description="List of applicant's social accounts")


class ApplicantVacancySplitResponse(BaseModel):
    id: int = Field(..., description="Applicant log ID")
    applicant: int = Field(..., description="Applicant ID")
    status: int = Field(..., description="Account vacancy status ID")
    vacancy_id: int = Field(..., alias="vacancy", description="Child vacancy ID")
    parent_vacancy_id: int = Field(..., alias="vacancy_parent", description="Parent vacancy ID")

    class Config:
        allow_population_by_field_name = True
