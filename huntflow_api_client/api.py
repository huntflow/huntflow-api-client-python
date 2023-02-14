from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Callable, List, Optional

import httpx

from huntflow_api_client.event_hooks.response import raise_token_expired_hook
from huntflow_api_client.errors import TokenExpiredError


@dataclass(frozen=True)
class ApiTokens:
    access_token: str
    refresh_token: str


@dataclass
class HuntflowApiToken:
    access_token: str
    refresh_token: str
    will_expire_at: Optional[datetime]


class TokenIsRefreshing(Exception):
    pass


class HuntflowTokenProxyBase:
    def __init__(self, token: HuntflowApiToken) -> None:
        self.token = token

    async def get_auth_header(self) -> Dict[str, str]:
        """Add blocking waiting for free lock here if you need to
        synchronize token updates
        """
        return {"Authorization": f"Bearer {self.token.access_token}"}

    async def get_refresh_token_data(self) -> Dict:
        return {"refresh_token": self.token.refresh_token}

    async def update_by_refresh_result(self, refresh_result: Dict) -> None:
        """Save updated token to a persistent storage here if you need it"""
        token = self.token
        now = datetime.now()
        token.access_token = refresh_result["access_token"]
        token.refresh_token = refresh_result["refresh_token"] or token.refresh_token
        token.will_expire_at = now + timedelta(seconds=refresh_result["expires_in"])

    async def lock_for_update(self):
        """If you have to synchronize token refreshing across several
        instances, then implement here non-blocking lock acquiring.
        If the lock is already acquired, then raise TokenIsRefreshing error.
        """
        pass

    async def release_lock(self):
        """Release lock if you have acquired it in lock_for_update method"""
        pass


class HuntflowAPI:
    def __init__(
        self,
        base_url: str,
        # Specify one of this: token or token_proxy
        token: Optional[HuntflowApiToken],
        token_proxy: Optional[HuntflowTokenProxyBase],
        auto_refresh_tokens: bool = False,
        request_event_hooks: List[Callable] = None,
        response_event_hooks: List[Callable] = None,
    ):
        assert token or token_proxy
        if not token:
            assert token_proxy
            token = token_proxy.token
        self.base_url = base_url
        self.token_proxy = token_proxy or HuntflowTokenProxyBase(token)

        self._request_event_hooks = request_event_hooks or []
        self._response_event_hooks = response_event_hooks or []

        if auto_refresh_tokens:
            if not token.refresh_token:
                raise ValueError("Refresh token is required.")
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

    async def run_token_refresh(self) -> None:
        try:
            await self.token_proxy.lock_for_update()
        except TokenIsRefreshing:
            return

        try:
            refresh_data = await self.token_proxy.get_refresh_token_data()
            async with self.http_client as client:
                response = await client.post(
                    "/v2/token/refresh", json=refresh_data,
                )
            await self.token_proxy.update_by_refresh_result(response.json())
        finally:
            await self.token_proxy.release_lock()

    async def _autorefresh_token(self, *args, **kwargs):
        try:
            response = await self._request(*args, **kwargs)
            return response
        except TokenExpiredError:
            await self.run_token_refresh()
            response = await self._request(*args, **kwargs)
            return response
