from datetime import datetime

from pydantic import BaseModel, Field


class ApplicantVacancyOffer(BaseModel):
    id: int = Field(..., description="Offer ID")
    account_applicant_offer: int = Field(..., description="Organization's offer ID")
    created: datetime = Field(..., description="Date and time of creating an offer")
