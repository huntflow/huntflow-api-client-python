from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ApplicantResponseVacancy(BaseModel):
    id: int = Field(..., description="Vacancy ID")
    position: str = Field(..., description="The name of the vacancy (occupation)")


class ApplicantResponseVacancyExternal(BaseModel):
    id: int = Field(..., description="Publication ID")
    foreign: str = Field(..., description="Foreign publication ID (from job site)")


class ApplicantResponse(BaseModel):
    id: int = Field(..., description="Response ID")
    foreign: str = Field(..., description="Foreign response ID (from job site)")
    created: datetime
    applicant_external: int = Field(..., description="Resume ID")
    vacancy: ApplicantResponseVacancy = Field(..., description="Vacancy")
    vacancy_external: ApplicantResponseVacancyExternal = Field(
        ...,
        description="Publication of a vacancy for which an applicant responded",
    )


class ApplicantResponsesListResponse(BaseModel):
    items: List[ApplicantResponse] = Field(..., description="List of applicant's responses")
    next_page_cursor: Optional[str] = Field(None, description="Next page cursor")
