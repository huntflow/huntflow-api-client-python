from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from huntflow_api_client.models.consts import RecommendationStatus


class RecommendationItem(BaseModel):
    id: int = Field(..., description="Recommendation ID")
    vacancy_id: int = Field(..., description="Vacancy ID")
    applicant_id: int = Field(..., description="Applicant ID")
    rank: int = Field(..., description="Position of the recommendation in the ranking list.")
    created_at: datetime = Field(
        ...,
        description="Date and time when the recommendation was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Date and time when the recommendation was last updated.",
    )
    resolved_by_user: Optional[int] = Field(
        None,
        description="ID of the recruiter who resolved recommendation. null if not processed yet.",
    )
    status: Optional[RecommendationStatus] = Field(
        None,
        description="Current status of the recommendation. null if not processed yet.",
    )


class RecommendationListResponse(BaseModel):
    items: List[RecommendationItem]
    next_page_cursor: Optional[str] = None
