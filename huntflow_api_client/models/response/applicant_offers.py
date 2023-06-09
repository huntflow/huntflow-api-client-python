from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class ApplicantVacancyOffer(BaseModel):
    id: int = Field(..., description="Offer ID")
    account_applicant_offer: int = Field(..., description="Organization's offer ID")
    created: datetime = Field(..., description="Date and time of creating an offer")


class ApplicantVacancyOfferResponse(ApplicantVacancyOffer):
    values: Dict = Field(
        ...,
        description=(
            "Offer values (fields). "
            "The composition of the values depends on the organization's offer settings."
        ),
    )
