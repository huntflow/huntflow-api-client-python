import typing as t

import httpx

from huntflow_api_client_python.serializers.response.info import OrganizationInfoResponse
from huntflow_api_client_python.serializers.response.applicants import (
    ApplicantCreateResponse,
    ApplicantUpdateResponse,
    ApplicantVacancySplitResponse
)
from huntflow_api_client_python.serializers.request.applicants import (
    ApplicantCreateRequest,
    ApplicantUpdateRequest,
    ApplicantVacancySplitRequest
)


class HuntflowApi:
    def __init__(
        self,
        base_url: str,
        token: str,
        response_event_hooks: t.List[t.Callable] = None,
        request_event_hooks: t.List[t.Callable] = None,
    ):
        self.base_url = base_url
        self.token = token
        self.response_event_hooks = response_event_hooks or []
        self.request_event_hooks = request_event_hooks or []

    @property
    def client(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        http_client = httpx.AsyncClient(base_url=self.base_url, headers=headers)
        http_client.event_hooks["response"] = self.response_event_hooks
        http_client.event_hooks["request"] = self.request_event_hooks
        return http_client

    async def get_organization(self, account_id: int) -> OrganizationInfoResponse:
        async with self.client as client:
            response = await client.get(f"/v2/accounts/{account_id}")
        result = response.json()
        return OrganizationInfoResponse(**result)

    async def create_applicant(
        self,
        account_id: int,
        data: ApplicantCreateRequest
    ) -> ApplicantCreateResponse:
        data = data.json()
        async with self.client as client:
            response = await client.post(f"/v2/accounts/{account_id}/applicants", data=data)
        result = response.json()
        return ApplicantCreateResponse(**result)

    async def update_applicant(
        self,
        account_id: int,
        applicant_id: int,
        data: ApplicantUpdateRequest
    ) -> ApplicantUpdateResponse:
        data = data.json()
        async with self.client as client:
            response = await client.patch(
                f"/v2/accounts/{account_id}/applicants/{applicant_id}",
                data=data
            )
        result = response.json()
        return ApplicantUpdateResponse(**result)

    async def delete_applicant(self, account_id: int, applicant_id: int):
        async with self.client as client:
            await client.delete(f"/v2/accounts/{account_id}/applicants/{applicant_id}")

    async def split_applicant_to_vacancy(
        self,
        account_id: int,
        vacancy_id: int,
        data: ApplicantVacancySplitRequest
    ) -> ApplicantVacancySplitResponse:
        data = data.json()
        async with self.client as client:
            response = await client.put(
                f"/v2/accounts/{account_id}/applicants/vacancy/{vacancy_id}/split",
                data=data
            )
        result = response.json()
        return ApplicantVacancySplitResponse(**result)
