from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, PositiveInt

from huntflow_api_client.models.common import EditedFillQuota, FillQuota, JsonRequestModel, Vacancy


class VacancyListState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    HOLD = "HOLD"


class VacancyUpdateState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    HOLD = "HOLD"


class VacancyCreateState(str, Enum):
    OPEN = "OPEN"


class VacancyCreateRequest(Vacancy, JsonRequestModel):
    account_applicant_offer: Optional[PositiveInt] = Field(
        None,
        description="Organization offer ID",
        example=10,
    )
    state: VacancyCreateState = Field(  # type: ignore
        VacancyCreateState.OPEN,
        description="The state of a vacancy",
    )
    coworkers: Optional[List[PositiveInt]] = Field(
        None,
        description="List of coworkers working with a vacancy",
        example=[1, 2],
    )
    body: Optional[str] = Field(
        None,
        description="The responsibilities for a vacancy in HTML format",
        example="<p>Test body</p>",
    )
    requirements: Optional[str] = Field(
        None,
        description="The requirements for a vacancy in HTML format",
        example="<p>Test requirements</p>",
    )
    conditions: Optional[str] = Field(
        None,
        description="The conditions for a vacancy in HTML format",
        example="<p>Test conditions</p>",
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="List of file IDs attached to a vacancy.",
        example=[1, 2, 3],
    )
    fill_quotas: List[FillQuota] = Field(..., max_items=1, description="Fill quota ID")

    class Config:
        extra = "allow"


class VacancyUpdateRequest(Vacancy, JsonRequestModel):
    body: Optional[str] = Field(
        None,
        description="The responsibilities for a vacancy in HTML format",
        example="<p>Test body</p>",
    )
    requirements: Optional[str] = Field(
        None,
        description="The requirements for a vacancy in HTML format",
        example="<p>Test requirements</p>",
    )
    conditions: Optional[str] = Field(
        None,
        description="The conditions for a vacancy in HTML format",
        example="<p>Test conditions</p>",
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="The list of files attached to a vacancy",
    )
    fill_quotas: Optional[List[EditedFillQuota]] = Field(None, description="Fill quota ID")
    account_vacancy_hold_reason: Optional[PositiveInt] = Field(
        None,
        description="Vacancy hold reason ID",
        example=12,
    )
    account_vacancy_close_reason: Optional[PositiveInt] = Field(
        None,
        description="Vacancy close reason ID",
        example=15,
    )

    class Config:
        extra = "allow"


class VacancyUpdatePartialRequest(VacancyUpdateRequest):
    position: Optional[str] = Field(  # type: ignore
        None,
        description="The name of the vacancy (occupation)",
        example="Developer",
    )


class VacancyMemberPermission(BaseModel):
    permission: str = Field(..., description="Permission ID")
    value: Optional[Union[PositiveInt, str]] = Field(None, description="Vacancy status ID")


class VacancyMemberCreateRequest(JsonRequestModel):
    permissions: Optional[List[VacancyMemberPermission]] = Field(
        description="List of permissions (if member type is `watcher`)",
    )
