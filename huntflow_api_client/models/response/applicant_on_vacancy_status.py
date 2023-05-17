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
