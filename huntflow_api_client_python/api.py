import typing as t

import httpx

from huntflow_api_client_python.models.response.tags import AccountTagResponse
from huntflow_api_client_python.models.request.tags import CreateAccountTagRequest


class HuntflowAPI:
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
    def client(self) -> httpx.AsyncClient:
        headers = {"Authorization": f"Bearer {self.token}"}
        http_client = httpx.AsyncClient(base_url=self.base_url, headers=headers)
        http_client.event_hooks["response"] = self.response_event_hooks
        http_client.event_hooks["request"] = self.request_event_hooks
        return http_client

    async def get_account_tag(self, account_id: int, tag_id: int) -> AccountTagResponse:
        async with self.client as client:
            response = await client.get(f"/v2/accounts/{account_id}/tags/{tag_id}")
        result = response.json()
        return AccountTagResponse(**result)

    async def create_account_tag(
        self,
        account_id: int,
        data: CreateAccountTagRequest
    ) -> AccountTagResponse:
        async with self.client as client:
            response = await client.post(
                f"/v2/accounts/{account_id}/tags",
                json=data.jsonable_dict()
            )
        result = response.json()
        return AccountTagResponse(**result)

    async def update_account_tag(
        self,
        account_id: int,
        tag_id: int,
        data: CreateAccountTagRequest
    ) -> AccountTagResponse:
        async with self.client as client:
            response = await client.put(
                f"/v2/accounts/{account_id}/tags/{tag_id}",
                json=data.jsonable_dict()
            )
        result = response.json()
        return AccountTagResponse(**result)

    async def delete_account_tag(self, account_id: int, tag_id: int) -> None:
        async with self.client as client:
            await client.delete(f"/v2/accounts/{account_id}/tags/{tag_id}")
