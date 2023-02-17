from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Callable, List, Optional, Type

import httpx

from huntflow_api_client.event_hooks.response import raise_token_expired_hook
from huntflow_api_client.errors import TokenExpiredError
from huntflow_api_client.token_proxy import (
    AbstractTokenProxy,
    HuntflowApiToken,
    HuntflowTokenProxyBase,
)


class TokenIsRefreshing(Exception):
    pass


class HuntflowAPI:
    def __init__(
        self,
        base_url: str,
        # Specify one of this: token or token_proxy
        token: Optional[HuntflowApiToken],
        token_proxy: Optional[AbstractTokenProxy],
        auto_refresh_tokens: bool = False,
        request_event_hooks: List[Callable] = None,
        response_event_hooks: List[Callable] = None,
        refresh_token_lock: Optional[Callable] = None,
        release_refresh_lock: Optional[Callable] = None,
        already_locked_exception_cls: Optional[Type[Exception]] = None,
    ):
        if token_proxy is None:
            if token is None:
                raise ValueError("Parameters token and token_proxy can't be None at the same time")
            token_proxy = HuntflowTokenProxyBase(token)
        self.token_proxy = token_proxy
        self.base_url = base_url

        self._request_event_hooks = request_event_hooks or []
        self._response_event_hooks = response_event_hooks or []
        is_invalid_arguments_for_refresh_lock = (
            (release_refresh_lock is None or already_locked_exception_cls is None)
            and refresh_token_lock is not None
        )
        if is_invalid_arguments_for_refresh_lock:
            raise Exception(
                "If refresh_token_lock is specified, then you have to provide "
                "release_refresh_lock and already_locked_exception_cls also"
            )
        self._refresh_token_lock = refresh_token_lock
        self._release_refresh_lock = release_refresh_lock
        self._already_locked_exception_cls = already_locked_exception_cls

        if auto_refresh_tokens:
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
        headers.update(await self.token_proxy.get_auth_header())
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

    async def _lock_for_update(self) -> bool:
        if self._refresh_token_lock is None:
            return True
        try:
            await self._refresh_token_lock()
        except self._already_locked_exception_cls:
            return False
        return True

    async def _release_lock_for_update(self):
        if self._release_refresh_lock is None:
            return
        await self._release_refresh_lock()

    async def run_token_refresh(self) -> None:
        if not await self._lock_for_update():
            return

        try:
            refresh_data = await self.token_proxy.get_refresh_token_data()
            async with self.http_client as client:
                response = await client.post(
                    "/v2/token/refresh", json=refresh_data,
                )
            await self.token_proxy.update_by_refresh_result(response.json())
        finally:
            await self._release_lock_for_update()

    async def _autorefresh_token(self, *args, **kwargs):
        try:
            response = await self._request(*args, **kwargs)
            return response
        except TokenExpiredError:
            await self.run_token_refresh()
            response = await self._request(*args, **kwargs)
            return response
