from typing import Callable, List, Optional

import httpx
from pydantic import BaseModel


class RefreshedTokens(BaseModel):
    access_token: str
    refresh_token: str


class HuntflowAPI:
    def __init__(
        self,
        base_url: str,
        access_token: str,
        refresh_token: Optional[str] = None,
        request_event_hooks: List[Callable] = None,
        response_event_hooks: List[Callable] = None,
    ):
        self.base_url = base_url
        self.access_token = access_token
        self.refresh_token = refresh_token

        request_event_hooks = request_event_hooks or []
        response_event_hooks = response_event_hooks or []

        self.http_client = self.init_http_client(request_event_hooks, response_event_hooks)

    def init_http_client(
        self,
        request_event_hooks: List[Callable],
        response_event_hooks: List[Callable],
    ) -> httpx.AsyncClient:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        http_client = httpx.AsyncClient(base_url=self.base_url, headers=headers)
        http_client.event_hooks["request"] = request_event_hooks
        http_client.event_hooks["response"] = response_event_hooks
        return http_client

    async def request(
        self,
        method: str,
        path: str,
        *,
        data=None,
        files=None,
        json=None,
        params=None,
        headers=None,
        timeout=None,
    ) -> httpx.Response:
        async with self.http_client as client:
            response = await client.request(
                method,
                path,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                timeout=timeout,
            )
        return response

    async def run_token_refresh(
        self, refresh_token: str = None, pre_cb: Callable = None, post_cb: Callable = None,
    ) -> RefreshedTokens:
        refresh_token = refresh_token or self.refresh_token
        if not refresh_token:
            raise ValueError("Refresh token is required.")

        if pre_cb:
            await pre_cb(refresh_token)

        async with self.http_client as client:
            response = await client.post(
                "/v2/token/refresh", json={"refresh_token": refresh_token},
            )

        tokens = RefreshedTokens(**response.json())
        self.access_token = tokens.access_token
        self.refresh_token = tokens.refresh_token

        if post_cb:
            await post_cb(tokens)

        return tokens
