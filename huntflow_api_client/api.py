from dataclasses import dataclass
from typing import Callable, List, Optional

import httpx

from huntflow_api_client.event_hooks.response import raise_token_expired_hook
from huntflow_api_client.utils.autorefresh import autorefresh_tokens


@dataclass(frozen=True)
class ApiTokens:
    access_token: str
    refresh_token: str


class HuntflowAPI:
    def __init__(
        self,
        base_url: str,
        access_token: str,
        refresh_token: Optional[str] = None,
        auto_refresh_tokens: bool = False,
        request_event_hooks: List[Callable] = None,
        response_event_hooks: List[Callable] = None,
    ):
        self.base_url = base_url
        self.access_token = access_token
        self.refresh_token = refresh_token

        self._request_event_hooks = request_event_hooks or []
        self._response_event_hooks = response_event_hooks or []

        if auto_refresh_tokens:
            if not refresh_token:
                raise ValueError("Refresh token is required.")
            self._response_event_hooks.append(raise_token_expired_hook)
            self.request = autorefresh_tokens(self.request, self.run_token_refresh)

    @property
    def http_client(self) -> httpx.AsyncClient:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        http_client = httpx.AsyncClient(base_url=self.base_url, headers=headers)
        http_client.event_hooks["request"] = self._request_event_hooks
        http_client.event_hooks["response"] = self._response_event_hooks
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
    ) -> ApiTokens:
        refresh_token = refresh_token or self.refresh_token
        if not refresh_token:
            raise ValueError("Refresh token is required.")

        old_tokens = ApiTokens(access_token=self.access_token, refresh_token=refresh_token)
        if pre_cb:
            await pre_cb(tokens_for_refresh=old_tokens)

        async with self.http_client as client:
            response = await client.post(
                "/v2/token/refresh", json={"refresh_token": refresh_token},
            )

        new_tokens = ApiTokens(**response.json())
        self.access_token = new_tokens.access_token
        self.refresh_token = new_tokens.refresh_token

        if post_cb:
            await post_cb(old_tokens=old_tokens, new_tokens=new_tokens)

        return new_tokens
