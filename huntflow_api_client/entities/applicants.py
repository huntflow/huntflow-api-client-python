from typing import Any, Dict, List, Optional, Union

from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    GetEntityMixin,
    ListEntityMixin,
)
from huntflow_api_client.models.consts import AgreementState, ApplicantSearchField
from huntflow_api_client.models.request.applicants import (
    ApplicantCreateRequest,
    ApplicantUpdateRequest,
)
from huntflow_api_client.models.response.applicants import (
    ApplicantCreateResponse,
    ApplicantItem,
    ApplicantListResponse,
    ApplicantSearchByCursorResponse,
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
            params["agreement_state"] = agreement_state.value
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants",
            params=params,
        )
        return ApplicantListResponse.model_validate(response.json())

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
        return ApplicantCreateResponse.model_validate(response.json())

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
        return ApplicantItem.model_validate(response.json())

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
        return ApplicantItem.model_validate(response.json())

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

    async def search_by_cursor(
        self,
        account_id: int,
        next_page_cursor: Optional[str] = None,
        query: Optional[str] = None,
        tag: Optional[List[int]] = None,
        status: Optional[List[int]] = None,
        rejection_reason: Optional[List[int]] = None,
        vacancy: Union[List[int], None] = None,
        only_current_status: bool = False,
        account_source: Optional[List[int]] = None,
        field: ApplicantSearchField = ApplicantSearchField.all,
        count: int = 30,
    ) -> ApplicantSearchByCursorResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/search_by_cursor

        :param account_id: Organization ID
        :param next_page_cursor: A cursor to the next page,
            if specified, no other params will  be included
        :param query: Search query
        :param tag: List of tag ID
        :param status: List of vacancy status ID
        :param rejection_reason: List of rejection reason ID
        :param vacancy: List of vacancy ID's or None
            - None - no filter for vacancies
            - [] - empty list means applicant is not assigned to any vacancy
            - [1, 2, 3] - applicants assigned to specified vacancies
        :param only_current_status: If the value is set to True,
            then applicants who are currently at this status will be displayed.
        :param account_source: List of resume source ID
        :param field: Search field
        :param count: Number of items per page

        :return: Returns a list of found applicants and a cursor to the next page
        """

        path = f"/accounts/{account_id}/applicants/search_by_cursor"

        params: Dict[str, Any]
        if next_page_cursor is not None:
            params = {"next_page_cursor": next_page_cursor}
        else:
            params = {
                "tag": tag or [],
                "status": status or [],
                "rejection_reason": rejection_reason or [],
                "only_current_status": only_current_status,
                "field": field.value,
                "count": count,
                "account_source": account_source or [],
            }
            if query:
                params["q"] = query

            if vacancy is not None:
                params["vacancy"] = vacancy if vacancy else "null"

        response = await self._api.request("GET", path, params=params)
        return ApplicantSearchByCursorResponse.model_validate(response.json())
