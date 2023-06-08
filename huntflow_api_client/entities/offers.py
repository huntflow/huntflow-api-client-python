from huntflow_api_client.entities.base import BaseEntity, UpdateEntityMixin
from huntflow_api_client.models.request.offers import ApplicantOfferUpdate
from huntflow_api_client.models.response.offers import (
    AccountOfferResponse,
    AccountOffersListResponse,
    ApplicantVacancyOfferResponse,
)


class Offer(BaseEntity, UpdateEntityMixin):
    async def get_account_offers(self, account_id: int) -> AccountOffersListResponse:
        """
        API method reference: https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/offers

        :param account_id: Organization ID

        :return: List of organization's offers
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/offers")
        return AccountOffersListResponse.parse_obj(response.json())

    async def get_account_offers_with_schema(
        self,
        account_id: int,
        offer_id: int,
    ) -> AccountOfferResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/offers/-offer_id-

        :param account_id: Organization ID
        :param offer_id: Offer ID

        :return: Organization's offer with a schema of values
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/offers/{offer_id}")
        return AccountOfferResponse.parse_obj(response.json())

    async def get_pdf(self, account_id: int, applicant_id: int, offer_id: int) -> bytes:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/offers/-offer_id-/pdf

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param offer_id: Offer ID

        :return: An applicant offer in bytes.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}/offers/{offer_id}/pdf",
        )
        return response.content

    async def update(
        self,
        account_id: int,
        applicant_id: int,
        offer_id: int,
        data: ApplicantOfferUpdate,
    ) -> ApplicantVacancyOfferResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/applicants/-applicant_id-/offers/-offer_id-

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param offer_id: Offer ID
        :param data: Data for updating offer

        :return: Updated applicant's offer.
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/applicants/{applicant_id}/offers/{offer_id}",
            json=data.jsonable_dict(),
        )
        return ApplicantVacancyOfferResponse.parse_obj(response.json())

    async def get_applicant_on_vacancy_offer(
        self,
        account_id: int,
        applicant_id: int,
        vacancy_frame_id: int,
    ) -> ApplicantVacancyOfferResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/vacancy_frames/-vacancy_frame_id-/offer

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param vacancy_frame_id: Vacancy frame ID

        :return: Applicant's offer for vacancy with its values.
                The composition of the values depends on the organization's offer settings.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}"
            f"/vacancy_frames/{vacancy_frame_id}/offer",
        )
        return ApplicantVacancyOfferResponse.parse_obj(response.json())
