from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin, UpdateEntityMixin
from huntflow_api_client.models.request.applicant_offers import ApplicantOfferUpdate
from huntflow_api_client.models.response.applicant_offers import ApplicantVacancyOfferResponse


class ApplicantOffer(BaseEntity, UpdateEntityMixin, GetEntityMixin):
    async def get_pdf(self, account_id: int, applicant_id: int, offer_id: int) -> bytes:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/offers/-offer_id-/pdf

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param offer_id: Offer ID

        :return: An applicant offer in PDF format
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
        return ApplicantVacancyOfferResponse.model_validate(response.json())

    async def get(
        self,
        account_id: int,
        applicant_id: int,
        vacancy_frame_id: int,
        normalize: bool = False,
    ) -> ApplicantVacancyOfferResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/vacancy_frames/-vacancy_frame_id-/offer

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param vacancy_frame_id: Vacancy frame ID
        :param normalize: Expand dictionary values to objects

        :return: Applicant's offer for vacancy with its values.
                The composition of the values depends on the organization's offer settings.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}"
            f"/vacancy_frames/{vacancy_frame_id}/offer",
            params={"normalize": normalize},
        )
        return ApplicantVacancyOfferResponse.model_validate(response.json())
