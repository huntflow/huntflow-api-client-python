from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field, PositiveInt


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


class AccountOffer(BaseModel):
    id: PositiveInt = Field(..., description="Offer ID")
    name: str = Field(..., description="Offer name")
    active: bool = Field(..., description="Offer activity flag")
    template: str = Field(..., description="HTML template")


class AccountOfferResponse(AccountOffer):
    schema_: Dict = Field(..., description="Values schema", alias="schema")


class AccountOffersListResponse(BaseModel):
    items: List[AccountOffer] = Field(..., description="List of organization offers")
