from huntflow_api_client.entities.base import (
    BaseEntity,
    CRUDEntityMixin,
    ListEntityMixin,
    UpdateEntityMixin,
)
from huntflow_api_client.models.request.tags import (
    CreateAccountTagRequest,
    UpdateApplicantTagsRequest,
)
from huntflow_api_client.models.response.tags import (
    AccountTagResponse,
    AccountTagsListResponse,
    ApplicantTagsListResponse,
)


class AccountTag(BaseEntity, CRUDEntityMixin, ListEntityMixin):
    async def get(self, account_id: int, account_tag_id: int) -> AccountTagResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/tags/-tag_id-

        :param account_id: Organization ID
        :param account_tag_id: Tag ID
        :return: The specified tag
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/tags/{account_tag_id}")
        return AccountTagResponse.model_validate(response.json())

    async def create(
        self,
        account_id: int,
        account_tag: CreateAccountTagRequest,
    ) -> AccountTagResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/tags

        :param account_id: Organization ID
        :param account_tag: Tag data
        :return: Tag
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/tags",
            json=account_tag.jsonable_dict(exclude_none=True),
        )
        return AccountTagResponse.model_validate(response.json())

    async def update(
        self,
        account_id: int,
        account_tag_id: int,
        data: CreateAccountTagRequest,
    ) -> AccountTagResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/tags/-tag_id-

        :param account_id: Organization ID
        :param account_tag_id: Tag ID
        :param data: Tag data
        :return: Tag
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/tags/{account_tag_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return AccountTagResponse.model_validate(response.json())

    async def delete(self, account_id: int, account_tag_id: int) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/hooks/-webhook_id-

        :param account_id: Organization ID
        :param account_tag_id: Tag ID
        """
        await self._api.request(
            "DELETE",
            f"/accounts/{account_id}/tags/{account_tag_id}",
        )

    async def list(self, account_id: int) -> AccountTagsListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/tags

        :param account_id: Organization ID
        :return: List of tags in the organization.
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/tags")
        return AccountTagsListResponse.model_validate(response.json())


class ApplicantTag(BaseEntity, UpdateEntityMixin, ListEntityMixin):
    async def update(
        self,
        account_id: int,
        applicant_id: int,
        data: UpdateApplicantTagsRequest,
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
        return ApplicantTagsListResponse.model_validate(response.json())

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
        return ApplicantTagsListResponse.model_validate(response.json())
