from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, root_validator

from huntflow_api_client.models.common import File, PaginatedResponse, Vacancy, VacancyQuotaItem
from huntflow_api_client.models.consts import FieldType


class AccountVacancyRequestSchemaField(BaseModel):
    id: PositiveInt = Field(..., description="Field ID")
    type: FieldType = Field(..., description="Field type")
    title: Optional[str] = Field(None, description="Field title")
    required: bool = Field(False, description="Field required flag")
    order: int = Field(..., description="The order of the field on the form")
    values: Optional[List] = Field(
        None,
        description="List of possible values (for fields.py with `select` type)",
    )
    value: Optional[str] = Field(None, description="Default value")
    fields_: Optional[Dict[str, "AccountVacancyRequestSchemaField"]] = Field(
        None,
        description="Nested fields.py",
        alias="fields",
    )

    class Config:
        extra = Extra.allow


class AdditionalFieldsSchemaResponse(BaseModel):
    __root__: Dict[str, AccountVacancyRequestSchemaField]

    @root_validator(pre=True)
    def prepare_data(
        cls, values: Dict[str, AccountVacancyRequestSchemaField]  # noqa N805
    ) -> Dict[str, Dict[str, AccountVacancyRequestSchemaField]]:
        return {"__root__": values}


class VacancyItem(Vacancy):
    id: Optional[PositiveInt] = Field(None, description="Vacancy ID")
    created: datetime = Field(..., description="Date and time of creating a vacancy")
    additional_fields_list: List[str] = Field(
        [],
        description="List of additional field names. ",
    )
    multiple: Optional[bool] = Field(
        None,
        description="Flag indicating if this vacancy is a " "multiple",
    )
    parent: Optional[PositiveInt] = Field(None, description="Vacancy parent ID")
    account_vacancy_status_group: Optional[PositiveInt] = Field(
        None,
        description="Vacancy status group ID",
    )

    class Config:
        extra = "allow"

    def dict(self, *args, **kwargs):  # type: ignore
        include = set(self.__fields__) | set(self.additional_fields_list)
        return super().dict(include=include)


class VacancyListResponse(PaginatedResponse):
    total_items: Optional[int] = Field(..., description="Total number of items")
    items: List[VacancyItem]


class VacancyChild(VacancyItem):
    """Child vacancy for multivacancy"""

    updated: Optional[datetime] = Field(None, description="Date and time of updating a vacancy")
    body: Optional[str] = Field(
        None,
        description="The responsibilities for a vacancy in HTML format",
    )
    requirements: Optional[str] = Field(
        None,
        description="The requirements for a vacancy in HTML format",
    )
    conditions: Optional[str] = Field(
        None,
        description="The conditions for a vacancy in HTML format",
    )
    files: List[File]
    source: Optional[str] = Field(
        None,
        description="Vacancy source ID if it was imported",
    )


class VacancyResponse(VacancyChild):
    blocks: Optional[List[VacancyChild]] = Field(
        [],
        description="Affiliate vacancies if vacancy is a multiple",
    )

    class Config:
        extra = "allow"

    def dict(self, *args, **kwargs):  # type: ignore
        include = set(self.__fields__) | set(self.additional_fields_list)
        return super().dict(include=include)


class VacancyCreateResponse(Vacancy):
    id: PositiveInt = Field(..., description="Vacancy ID")
    created: datetime = Field(..., description="Date and time of creating a vacancy")
    coworkers: Optional[List[PositiveInt]] = Field(
        None,
        description="List of coworkers working with a vacancy",
    )
    body: Optional[str] = Field(
        None,
        description="The responsibilities for a vacancy in HTML format",
    )
    requirements: Optional[str] = Field(
        None,
        description="The requirements for a vacancy in HTML format",
    )
    conditions: Optional[str] = Field(
        None,
        description="The conditions for a vacancy in HTML format",
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="The list of file IDs attached to a vacancy",
    )
    account_vacancy_status_group: Optional[PositiveInt] = Field(
        None,
        description="Vacancy status group ID",
    )
    parent: Optional[int] = Field(None, description="Parent vacancy ID")
    source: Optional[str] = Field(None, description="Vacancy source ID if it was imported")
    multiple: bool = Field(False, description="Flag indicating if this vacancy is a multiple")
    vacancy_request: Optional[PositiveInt] = Field(
        None,
        description="Vacancy request ID",
    )

    class Config:
        extra = "ignore"


class LastVacancyFrameResponse(BaseModel):
    id: PositiveInt = Field(..., description="Vacancy frame ID")
    frame_begin: datetime = Field(..., description="Date and time of creating a frame")
    frame_end: Optional[datetime] = Field(None, description="Date and time of closing a frame")
    vacancy: PositiveInt = Field(..., description="Vacancy ID")
    hired_applicants: Optional[List[int]] = Field(None, description="Hired Applicant IDs")
    workdays_in_work: int = Field(..., description="How many working days the vacancy is in work")
    workdays_before_deadline: Optional[int] = Field(
        None,
        description="How many working days before deadline",
    )


class VacancyFrame(LastVacancyFrameResponse):
    next_id: Optional[int] = Field(None, description="The next frame ID")


class VacancyQuotaList(PaginatedResponse):
    total_items: Optional[int] = Field(None, description="Total number of items")
    items: List[VacancyQuotaItem]


class VacancyFramesListResponse(BaseModel):
    items: List[VacancyFrame]


class VacancyFrameQuotasResponse(BaseModel):
    items: List[VacancyQuotaItem]


class VacancyQuotasResponse(BaseModel):
    __root__: Dict[str, VacancyQuotaList] = Field(..., descriptions="Vacancy quotas")
