from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin, UpdateEntityMixin
from huntflow_api_client.models.request.applicant_tags import ApplicantTagsUpdateRequest
from huntflow_api_client.models.response.applicant_tags import ApplicantTagsListResponse


class ApplicantTag(BaseEntity, UpdateEntityMixin, ListEntityMixin):
    async def update(
        self,
        account_id: int,
        applicant_id: int,
        data: ApplicantTagsUpdateRequest,
    ) -> ApplicantTagsListResponse:
        """
        API method reference
           https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/applicants/-applicant_id-/tags

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param data: List of applicant's tags IDs
        :return: List of applicant's tags IDs.
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/applicants/{applicant_id}/tags",
            json=data.jsonable_dict(exclude_none=True),
        )
        return ApplicantTagsListResponse(**response.json())

    async def list(self, account_id: int, applicant_id: int) -> ApplicantTagsListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/tags

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :return: List of applicant's tags IDs.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}/tags",
        )
        return ApplicantTagsListResponse(**response.json())
