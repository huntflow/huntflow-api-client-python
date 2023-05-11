from typing import Any, Dict, Optional

from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    GetEntityMixin,
    ListEntityMixin,
)
from huntflow_api_client.models.consts import AgreementState
from huntflow_api_client.models.request.applicants import (
    ApplicantCreateRequest,
    ApplicantUpdateRequest,
)
from huntflow_api_client.models.response.applicants import (
    ApplicantCreateResponse,
    ApplicantItem,
    ApplicantListResponse,
)


class Applicant(BaseEntity, ListEntityMixin, CreateEntityMixin, GetEntityMixin):
    async def list(
        self,
        account_id: int,
        count: Optional[int] = 30,
        page: Optional[int] = 1,
        status: Optional[int] = None,
        vacancy_id: Optional[int] = None,
        agreement_state: Optional[AgreementState] = None,
    ) -> ApplicantListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants

        :param account_id: Organization ID
        :param count: Number of items per page
        :param page: Page number
        :param status: Vacancy status ID
        :param vacancy_id: Vacancy ID
        :param agreement_state: Agreement's state of applicant to personal data processing.
            Available if the Personal Data module is enabled for organization.
            Cannot be supplied if the status parameter is passed.
        :return: List of applicants with pagination
        """
        params: Dict[str, Any] = {"count": count, "page": page}
        if status:
            params["status"] = status
        if vacancy_id:
            params["vacancy_id"] = vacancy_id
        if agreement_state:
            params["agreement_state"] = agreement_state
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants",
            params=params,
        )
        return ApplicantListResponse.parse_obj(response.json())

    async def create(
        self,
        account_id: int,
        data: ApplicantCreateRequest,
    ) -> ApplicantCreateResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/applicants

        :param account_id: Organization ID
        :param data: Applicant data
        :return: The created applicant
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/applicants",
            json=data.jsonable_dict(exclude_none=True),
        )
        return ApplicantCreateResponse.parse_obj(response.json())

    async def get(self, account_id: int, applicant_id: int) -> ApplicantItem:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :return: The specified applicant
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}",
        )
        return ApplicantItem.parse_obj(response.json())

    async def patch(
        self,
        account_id: int,
        applicant_id: int,
        data: ApplicantUpdateRequest,
    ) -> ApplicantItem:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#patch-/accounts/-account_id-/applicants/-applicant_id-

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param data: Applicant data
        :return: The created applicant
        """
        response = await self._api.request(
            "PATCH",
            f"/accounts/{account_id}/applicants/{applicant_id}",
            json=data.jsonable_dict(exclude_none=True),
        )
        return ApplicantItem.parse_obj(response.json())

    async def delete(self, account_id: int, applicant_id: int) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/applicants/-applicant_id-

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        """
        await self._api.request(
            "DELETE",
            f"/accounts/{account_id}/applicants" f"/{applicant_id}",
        )
