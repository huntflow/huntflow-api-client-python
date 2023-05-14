from typing import Any, Dict, List, Optional, Union

from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    GetEntityMixin,
    ListEntityMixin,
)
from huntflow_api_client.models.consts import AgreementState, ApplicantLogType, ApplicantSearchField
from huntflow_api_client.models.request.applicants import (
    ApplicantCreateRequest,
    ApplicantUpdateRequest,
    CreateApplicantLogRequest,
)
from huntflow_api_client.models.response.applicants import (
    ApplicantCreateResponse,
    ApplicantItem,
    ApplicantListResponse,
    ApplicantLogResponse,
    ApplicantSearchByCursorResponse,
    ApplicantSearchResponse,
    CreateApplicantLogResponse,
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

    async def search(
        self,
        account_id: int,
        q: Optional[str] = None,
        tag: Optional[List[int]] = None,
        status: Optional[List[int]] = None,
        rejection_reason: Optional[List[int]] = None,
        vacancy: Union[List[int], str, None] = None,
        account_source: Optional[List[int]] = None,
        only_current_status: bool = False,
        field: ApplicantSearchField = ApplicantSearchField.all,
        count: int = 30,
        page: int = 1,
    ) -> ApplicantSearchResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/search

        :param account_id: Organization ID
        :param q: Search query
        :param tag: List of tag ID
        :param status: List of vacancy status ID
        :param rejection_reason: List of rejection reason ID
        :param vacancy: List of vacancy ID or 'null', If you pass a 'null' value,
            then applicants who have not been added to any vacancy will be displayed
        :param account_source: List of resume source ID
        :param only_current_status: If the value is set to True,
            then applicants who are currently at this status will be displayed.
        :param field: Search field, Allowed: all ┃ education ┃ experience ┃ position
        :param count: Number of items per page
        :param page: Page number

        :return: List of found applicants. Limited by 20k items
        """
        path = f"/accounts/{account_id}/applicants/search"
        params = {
            "tag": tag or [],
            "status": status or [],
            "rejection_reason": rejection_reason or [],
            "vacancy": vacancy or [],
            "only_current_status": only_current_status,
            "field": field.value,
            "count": count,
            "page": page,
            "account_source": account_source or [],
        }
        if q:
            params["q"] = q

        response = await self._api.request("GET", path, params=params)
        return ApplicantSearchResponse.parse_obj(response.json())

    async def search_by_cursor(
        self,
        account_id: int,
        next_page_cursor: Optional[str] = None,
        q: Optional[str] = None,
        tag: Optional[List[int]] = None,
        status: Optional[List[int]] = None,
        rejection_reason: Optional[List[int]] = None,
        vacancy: Union[List[int], str, None] = None,
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
        :param q: Search query
        :param tag: List of tag ID
        :param status: List of vacancy status ID
        :param rejection_reason: List of rejection reason ID
        :param vacancy: List of vacancy ID or 'null', If you pass a 'null' value,
            then applicants who have not been added to any vacancy will be displayed
        :param only_current_status: If the value is set to True,
            then applicants who are currently at this status will be displayed.
        :param account_source: List of resume source ID
        :param field: Search field
        :param count: Number of items per page

        :return: Returns a list of found applicants and a cursor to the next page
        """
        path = f"/accounts/{account_id}/applicants/search_by_cursor"
        params = {
            "tag": tag or [],
            "status": status or [],
            "rejection_reason": rejection_reason or [],
            "vacancy": vacancy or [],
            "only_current_status": only_current_status,
            "field": field.value,
            "count": count,
            "account_source": account_source or [],
        }
        if q:
            params["q"] = q
        if next_page_cursor is not None:
            params = {"next_page_cursor": next_page_cursor}

        response = await self._api.request("GET", path, params=params)
        return ApplicantSearchByCursorResponse.parse_obj(response.json())

    async def log_list(
        self,
        account_id: int,
        applicant_id: int,
        type_: Optional[ApplicantLogType] = None,
        vacancy: Optional[int] = None,
        personal: bool = False,
        count: int = 30,
        page: int = 1,
    ) -> ApplicantLogResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/logs

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param type_: Log type
        :param vacancy: If supplied, only logs related to the specified vacancy will be returned
        :param personal: If supplied, only logs not related to any vacancy will be returned
        :param count: Number of items per page
        :param page: Page number

        :return: List of applicant's worklog
        """
        path = f"/accounts/{account_id}/applicants/{applicant_id}/logs"
        params: Dict[str, Any] = {
            "personal": personal,
            "count": count,
            "page": page,
        }
        if type_:
            params["type"] = type_.value
        if vacancy:
            params["vacancy"] = vacancy

        response = await self._api.request("GET", path, params=params)
        return ApplicantLogResponse.parse_obj(response.json())

    async def create_worklog_note(
        self,
        account_id: int,
        applicant_id: int,
        request_data: CreateApplicantLogRequest,
    ) -> CreateApplicantLogResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/applicants/-applicant_id-/logs

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param request_data: Request body

        :return: Created log data
        """
        path = f"/accounts/{account_id}/applicants/{applicant_id}/logs"
        response = await self._api.request(
            "POST",
            path,
            json=request_data.jsonable_dict(exclude_none=True),
        )
        return CreateApplicantLogResponse.parse_obj(response.json())