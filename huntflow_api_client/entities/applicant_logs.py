from typing import Any, Dict, Optional

from huntflow_api_client.entities.base import BaseEntity, CreateEntityMixin, ListEntityMixin
from huntflow_api_client.models.consts import ApplicantLogType
from huntflow_api_client.models.request.applicant_logs import CreateApplicantLogRequest
from huntflow_api_client.models.response.applicant_logs import (
    ApplicantLogResponse,
    CreateApplicantLogResponse,
)


class ApplicantLog(BaseEntity, ListEntityMixin, CreateEntityMixin):
    async def list(
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
        return ApplicantLogResponse.model_validate(response.json())

    async def create(
        self,
        account_id: int,
        applicant_id: int,
        data: CreateApplicantLogRequest,
    ) -> CreateApplicantLogResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/applicants/-applicant_id-/logs

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param data: Data for creating worklog

        :return: Created applicant's worklog
        """

        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/applicants/{applicant_id}/logs",
            json=data.jsonable_dict(exclude_none=True),
        )
        return CreateApplicantLogResponse.model_validate(response.json())
