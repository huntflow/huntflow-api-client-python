import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

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
    )
    state: VacancyCreateState = Field(  # type: ignore
        VacancyCreateState.OPEN,
        description="The state of a vacancy",
    )
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
        description="List of file IDs attached to a vacancy.",
    )
    fill_quotas: List[FillQuota] = Field(..., max_length=1, description="Fill quota ID")

    model_config = ConfigDict(extra="allow")


class VacancyUpdateRequest(Vacancy, JsonRequestModel):
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
        description="The list of files attached to a vacancy",
    )
    fill_quotas: Optional[List[EditedFillQuota]] = Field(None, description="Fill quota ID")
    account_vacancy_hold_reason: Optional[PositiveInt] = Field(
        None,
        description="Vacancy hold reason ID",
    )
    account_vacancy_close_reason: Optional[PositiveInt] = Field(
        None,
        description="Vacancy close reason ID",
    )

    model_config = ConfigDict(extra="allow")


class VacancyUpdatePartialRequest(VacancyUpdateRequest):
    position: Optional[str] = Field(  # type: ignore
        None,
        description="The name of the vacancy (occupation)",
    )


class VacancyMemberPermission(BaseModel):
    permission: str = Field(..., description="Permission ID")
    value: Optional[Union[PositiveInt, str]] = Field(None, description="Vacancy status ID")


class VacancyMemberCreateRequest(JsonRequestModel):
    permissions: Optional[List[VacancyMemberPermission]] = Field(
        description="List of permissions (if member type is `watcher`)",
    )


class VacancyStateChangeRequestBase(BaseModel):
    date: Optional[datetime.date] = Field(None, description="Action date")
    comment: Optional[str] = Field(None, description="Comment")
    unpublish_all: Optional[bool] = Field(
        False,
        description="Remove a vacancy from all publications",
    )


class VacancyCloseRequest(VacancyStateChangeRequestBase, JsonRequestModel):
    account_vacancy_close_reason: Optional[PositiveInt] = Field(
        None,
        description="Vacancy close reason ID",
    )


class VacancyHoldRequest(VacancyStateChangeRequestBase, JsonRequestModel):
    account_vacancy_hold_reason: Optional[PositiveInt] = Field(
        None,
        description="Vacancy hold reason ID",
    )
