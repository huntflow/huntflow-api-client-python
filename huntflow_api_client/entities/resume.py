from huntflow_api_client.entities.base import (
    BaseEntity,
    DeleteEntityMixin,
    GetEntityMixin,
    UpdateEntityMixin,
)
from huntflow_api_client.models.request.applicants import ApplicantResumeUpdateRequest
from huntflow_api_client.models.response.applicants import ApplicantSourcesResponse
from huntflow_api_client.models.response.resume import ApplicantResumeResponse


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
        :param external_id: External ID
        :return: An applicant resume
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}/externals/{external_id}",
        )
        return ApplicantResumeResponse.parse_obj(response.json())

    async def get_resume_sources(self, account_id: int) -> ApplicantSourcesResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/sources

        :param account_id: Organization ID
        :return: List of applicant's resume sources
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/applicants/sources")
        return ApplicantSourcesResponse.parse_obj(response.json())

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
        :param external_id: External ID
        """
        await self._api.request(
            "DELETE", f"/accounts/{account_id}/applicants/{applicant_id}/externals/{external_id}",
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
        :param external_id: External ID
        :param data: Data for updating  specified applicant's resume.
        :return: An applicant resume
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/applicants/{applicant_id}/externals/{external_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return ApplicantResumeResponse.parse_obj(response.json())
