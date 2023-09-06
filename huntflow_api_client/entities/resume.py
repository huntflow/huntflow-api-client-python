from huntflow_api_client.entities.base import (
    BaseEntity,
    DeleteEntityMixin,
    GetEntityMixin,
    UpdateEntityMixin,
)
from huntflow_api_client.models.request.resume import ApplicantResumeUpdateRequest
from huntflow_api_client.models.response.resume import (
    ApplicantResumeResponse,
    ApplicantSourcesResponse,
)


class Resume(BaseEntity, GetEntityMixin, DeleteEntityMixin, UpdateEntityMixin):
    async def get(
        self,
        account_id: int,
        applicant_id: int,
        external_id: int,
    ) -> ApplicantResumeResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/externals/-external_id-

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param external_id: Resume ID
        :return: An applicant resume
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}/externals/{external_id}",
        )
        return ApplicantResumeResponse.model_validate(response.json())

    async def get_sources(self, account_id: int) -> ApplicantSourcesResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/sources

        :param account_id: Organization ID
        :return: List of applicant's resume sources
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/applicants/sources")
        return ApplicantSourcesResponse.model_validate(response.json())

    async def delete(
        self,
        account_id: int,
        applicant_id: int,
        external_id: int,
    ) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/applicants/-applicant_id-/externals/-external_id-

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param external_id: Resume ID
        """
        await self._api.request(
            "DELETE",
            f"/accounts/{account_id}/applicants/{applicant_id}/externals/{external_id}",
        )

    async def update(
        self,
        account_id: int,
        applicant_id: int,
        external_id: int,
        data: ApplicantResumeUpdateRequest,
    ) -> ApplicantResumeResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/applicants/-applicant_id-/externals/-external_id-

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param external_id: Resume ID
        :param data: Data for updating  specified applicant's resume.
        :return: An applicant resume
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/applicants/{applicant_id}/externals/{external_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return ApplicantResumeResponse.model_validate(response.json())

    async def get_pdf(
        self,
        account_id: int,
        applicant_id: int,
        external_id: int,
    ) -> bytes:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/externals/-external_id-/pdf

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param external_id: Resume ID
        :return: A pdf file of the applicant's resume
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}/externals/{external_id}/pdf",
        )
        return response.content
