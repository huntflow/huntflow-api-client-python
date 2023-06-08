from typing import Dict, List

from pydantic import BaseModel, Field, PositiveInt


class AccountOffer(BaseModel):
    id: PositiveInt = Field(..., description="Offer ID")
    name: str = Field(..., description="Offer name")
    active: bool = Field(..., description="Offer activity flag")
    template: str = Field(..., description="HTML template")


class AccountOfferResponse(AccountOffer):
    schema_: Dict = Field(..., description="Values schema", alias="schema")


class AccountOffersListResponse(BaseModel):
    items: List[AccountOffer] = Field(..., description="List of organization offers")
