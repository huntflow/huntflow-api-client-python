from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AddApplicantToVacancyResponse(BaseModel):
    id: int = Field(..., description="Binding ID")
    changed: datetime = Field(..., description="The date of recruitment stage change")
    vacancy_id: int = Field(..., alias="vacancy", description="Vacancy ID")
    status: int = Field(..., description="Vacancy status ID")
    rejection_reason: Optional[int] = Field(None, description="Rejection reason ID")

    model_config = ConfigDict(populate_by_name=True)


class ApplicantVacancySplitResponse(BaseModel):
    id: int = Field(..., description="Applicant log ID")
    applicant: int = Field(..., description="Applicant ID")
    status: int = Field(..., description="Account vacancy status ID")
    vacancy_id: int = Field(..., alias="vacancy", description="Child vacancy ID")
    parent_vacancy_id: int = Field(..., alias="vacancy_parent", description="Parent vacancy ID")

    model_config = ConfigDict(populate_by_name=True)
