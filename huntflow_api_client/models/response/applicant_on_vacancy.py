from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class VacancyStatus(BaseModel):
    id: int = Field(..., description="Vacancy status ID")
    type: str = Field(..., description="Status type")
    name: str = Field(..., description="Status name")
    removed: Optional[datetime] = Field(
        None,
        description="Date and time of removing an vacancy status",
    )
    order: int = Field(..., description="Order number")
    stay_duration: Optional[int] = Field(
        None,
        description=(
            "The allowed number of days of a applicant's stay at this status."
            "`null` means unlimited"
        ),
    )


class VacancyStatusesResponse(BaseModel):
    items: List[VacancyStatus]


class AddApplicantToVacancyResponse(BaseModel):
    id: int = Field(..., description="Binding ID", example=9)
    changed: datetime = Field(..., description="The date of recruitment stage change")
    vacancy_id: int = Field(..., alias="vacancy", description="Vacancy ID")
    status: int = Field(..., description="Vacancy status ID")
    rejection_reason: Optional[int] = Field(None, description="Rejection reason ID")

    class Config:
        allow_population_by_field_name = True


class ApplicantVacancySplitResponse(BaseModel):
    id: int = Field(..., description="Applicant log ID")
    applicant: int = Field(..., description="Applicant ID")
    status: int = Field(..., description="Account vacancy status ID")
    vacancy_id: int = Field(..., alias="vacancy", description="Child vacancy ID")
    parent_vacancy_id: int = Field(..., alias="vacancy_parent", description="Parent vacancy ID")

    class Config:
        allow_population_by_field_name = True
