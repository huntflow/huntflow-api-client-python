from typing import Callable, List, Optional

import httpx

from huntflow_api_client.errors import TokenExpiredError
from huntflow_api_client.event_hooks.response import raise_token_expired_hook
from huntflow_api_client.tokens import (
    AbstractTokenHandler,
    DummyTokenHandler,
    HuntflowApiTokens,
)


class HuntflowAPI:
    def __init__(
        self,
        base_url: str,
        *,
        # Specify one of this: api_tokens or token_handler
        api_tokens: Optional[HuntflowApiTokens] = None,
        tokens_handler: Optional[AbstractTokenHandler] = None,
        request_event_hooks: List[Callable] = None,
        response_event_hooks: List[Callable] = None,
    ):
        self.base_url = base_url
        if tokens_handler is None:
            if api_tokens is None:
                raise ValueError(
                    "Parameters api_tokens and token_handler "
                    "can not be None at the same time"
                )
            tokens_handler = DummyTokenHandler(api_tokens=api_tokens)

        self._tokens_handler = tokens_handler
        self._request_event_hooks = request_event_hooks or []
        self._response_event_hooks = response_event_hooks or []

        if tokens_handler.auto_refresh:
            self._response_event_hooks.append(raise_token_expired_hook)
            self._request = self.request
            self.request = self._autorefresh_token

    @property
    def http_client(self) -> httpx.AsyncClient:
        http_client = httpx.AsyncClient(base_url=self.base_url)
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
        headers = headers or {}
        headers.update(await self._tokens_handler.get_auth_header())
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

    async def run_token_refresh(self) -> None:
        if not self._tokens_handler.auto_refresh:
            return

        if not await self._tokens_handler.set_lock_for_update():
            return

        try:
            refresh_data = await self._tokens_handler.get_refresh_token_data()
            async with self.http_client as client:
                response = await client.post(
                    "/v2/token/refresh", json=refresh_data,
                )
            await self._tokens_handler.update_by_refresh_result(response.json())
        finally:
            await self._tokens_handler.release_lock_for_update()

    async def _autorefresh_token(self, *args, **kwargs):
        try:
            if self._tokens_handler.lock:
                async with self._tokens_handler.lock:
                    response = await self._request(*args, **kwargs)
                    return response
            else:
                response = await self._request(*args, **kwargs)
                return response
        except TokenExpiredError:
            await self.run_token_refresh()
            response = await self._request(*args, **kwargs)
            return response
