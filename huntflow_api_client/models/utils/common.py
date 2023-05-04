from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class VacancyState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    HOLD = "HOLD"
    REOPEN = "REOPEN"
    VACANCY_REQUEST_ATTACH = "VACANCY_REQUEST_ATTACH"
    RESUME = "RESUME"
    CREATED = "CREATED"


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
    id: Optional[PositiveInt] = Field(None, description="Fill quota ID", example=15)  # noqa A003
