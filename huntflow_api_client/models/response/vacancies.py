from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, root_validator

from huntflow_api_client.models.utils.common import Vacancy
from huntflow_api_client.models.utils.fields import FieldType, File
from huntflow_api_client.models.utils.pagination import ListResponseMixin


class AccountVacancyRequestSchemaField(BaseModel):
    id: PositiveInt = Field(..., description="Field ID")  # noqa A003
    type: FieldType = Field(..., description="Field type", example=FieldType.select)  # noqa A003
    title: Optional[str] = Field(None, description="Field title", example="Reason")
    required: bool = Field(False, description="Field required flag")
    order: int = Field(..., description="The order of the field on the form", example=1)
    values: Optional[List] = Field(
        None,
        description="List of possible values (for fields.py with `select` type)",
        example=["New position", "Replacing an employee"],
    )
    value: Optional[str] = Field(None, description="Default value", example="New position")
    fields_: Optional[dict[str, "AccountVacancyRequestSchemaField"]] = Field(
        None,
        description="Nested fields.py",
        alias="fields.py",
    )

    class Config:
        extra = Extra.allow


class AdditionalFieldsSchemaResponse(BaseModel):
    __root__: dict[str, AccountVacancyRequestSchemaField] = Field(
        ...,
        example={
            "reason": {
                "id": 50,
                "type": "select",
                "title": "Reason",
                "required": True,
                "order": 1,
                "values": ["New position", "Replacing an employee"],
                "value": None,
                "name": "reason",
                "account": 11,
            },
            "category": {
                "id": 51,
                "type": "dictionary",
                "title": "Category",
                "required": False,
                "order": 2,
                "values": None,
                "pass_to_report": False,
                "dictionary": "category",
                "name": "category",
                "account": 11,
                "availableOn": {"operator": "==", "field": "reason", "value": "New position"},
                "filterable": False,
            },
        },
    )

    @root_validator(pre=True)
    def prepare_data(self, values):
        return {"__root__": values}


class VacancyItem(Vacancy):
    id: PositiveInt = Field(None, description="Vacancy ID", example=150)  # noqa A003
    created: datetime = Field(..., description="Date and time of creating a vacancy")
    additional_fields_list: List[str] = Field(
        [],
        description=(
            "List of additional field names. "
            "[Getting a schema of additional fields]"
            "(/v2/docs#/Vacancies/get_additional_fields_schema_accounts"
            "__account_id__vacancies_additional_fields_get)"
        ),
        example=["deadline"],
    )
    multiple: bool = Field(None, description="Flag indicating if this vacancy is a multiple")
    parent: PositiveInt = Field(None, description="Vacancy parent ID", example=15)
    account_vacancy_status_group: PositiveInt = Field(
        None,
        description="Vacancy status group ID",
        example=12,
    )

    class Config:
        extra = "allow"

    def dict(self, *args, **kwargs):  # noqa A003
        include = set(self.__fields__) | set(self.additional_fields_list)
        return super().dict(include=include)


class VacancyListResponse(ListResponseMixin):
    items: List[VacancyItem]


class VacancyChild(VacancyItem):
    """Child vacancy for multivacancy"""

    updated: Optional[datetime] = Field(None, description="Date and time of updating a vacancy")
    body: str = Field(
        None,
        description="The responsibilities for a vacancy in HTML format",
        example="<p>Test body</p>",
    )
    requirements: str = Field(
        None,
        description="The requirements for a vacancy in HTML format",
        example="<p>Test requirements</p>",
    )
    conditions: str = Field(
        None,
        description="The conditions for a vacancy in HTML format",
        example="<p>Test conditions</p>",
    )
    files: List[File]
    source: Optional[str] = Field(
        None,
        description="Vacancy source ID if it was imported",
        example="0x5F22EC3F759E002B",
    )


class VacancyResponse(VacancyChild):
    blocks: Optional[List[VacancyChild]] = Field(
        [],
        description="Affiliate vacancies if vacancy is a multiple",
    )

    class Config:
        extra = "allow"

    def dict(self, *args, **kwargs):  # noqa A003
        include = set(self.__fields__) | set(self.additional_fields_list)
        return super().dict(include=include)


class VacancyCreateResponse(Vacancy):
    id: PositiveInt = Field(..., description="Vacancy ID", example=10)  # noqa A003
    created: datetime = Field(..., description="Date and time of creating a vacancy")
    coworkers: List[PositiveInt] = Field(
        None,
        description="List of coworkers working with a vacancy",
        example=[1, 2],
    )
    body: str = Field(
        None,
        description="The responsibilities for a vacancy in HTML format",
        example="<p>Test body</p>",
    )
    requirements: str = Field(
        None,
        description="The requirements for a vacancy in HTML format",
        example="<p>Test requirements</p>",
    )
    conditions: str = Field(
        None,
        description="The conditions for a vacancy in HTML format",
        example="<p>Test conditions</p>",
    )
    files: List[PositiveInt] = Field(
        None,
        description="The list of file IDs attached to a vacancy",
        example=[1, 2],
    )
    account_vacancy_status_group: Optional[PositiveInt] = Field(
        None,
        description="Vacancy status group ID",
        example=10,
    )
    parent: Optional[int] = Field(None, description="Parent vacancy ID", example=9)
    source: Optional[str] = Field(None, description="Vacancy source ID if it was imported")
    multiple: bool = Field(False, description="Flag indicating if this vacancy is a multiple")
    vacancy_request: Optional[PositiveInt] = Field(
        None,
        alias="vacancy_request",
        description="Vacancy request ID",
        example=3,
    )

    class Config:
        extra = "ignore"