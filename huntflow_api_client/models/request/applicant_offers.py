from typing import Dict

from pydantic import Field, PositiveInt

from huntflow_api_client.models.common import JsonRequestModel


class ApplicantOfferUpdate(JsonRequestModel):
    account_applicant_offer: PositiveInt = Field(..., description="Organization offer ID")
    values: Dict = Field(..., description="Offer values")
