import logging
from typing import Optional

import httpx

from huntflow_api_client.errors.errors import InvalidAccessTokenError, TokenExpiredError
from huntflow_api_client.errors.response_hooks import raise_for_status
from huntflow_api_client.tokens.proxy import AbstractTokenProxy, DummyHuntflowTokenProxy
from huntflow_api_client.tokens.token import ApiToken

logger = logging.getLogger(__name__)


class HuntflowAPI:
    def __init__(
        self,
        base_url: str = "https://api.huntflow.dev/v2",
        # Specify one of this: token or token_proxy
        token: Optional[ApiToken] = None,
        token_proxy: Optional[AbstractTokenProxy] = None,
        auto_refresh_tokens: bool = False,
    ):
        """API client.
        :param base_url: Base url for API (including schema and version prefix),
            like 'https://<api domain>/v2'
        :param token: Optional token structure with access token.
            Use it if you don't care about token refreshing
        :param token_proxy: Alternative way (see `token` param) to provide token.
            If you need to properly refresh tokens, then you should use this param
            instead of `token`. You can use `huntflow_api_client.tokens.proxy.HuntflowTokenProxy`
            or implement your own class for this,
            the class must implement AbstractTokenProxy interface.
            Also see usage example at `examples.api_client_with_simple_locks`.
        :param auto_refresh_tokens: If True then the client will handle token expiration.
            "Handle" means: catch token expiration errors and run token refresh request.
        """
        if token_proxy is None:
            if token is None:
                raise ValueError("Parameters token and token_proxy can't be None at the same time")
            token_proxy = DummyHuntflowTokenProxy(token)
        self._token_proxy: AbstractTokenProxy = token_proxy
        self.base_url = base_url

        self._autorefresh_tokens = auto_refresh_tokens

    @property
    def http_client(self) -> httpx.AsyncClient:
        http_client = httpx.AsyncClient(base_url=self.base_url)
        http_client.event_hooks["response"] = [raise_for_status]
        return http_client

    async def request(  # type: ignore[no-untyped-def]
        self,
        method: str,
        path: str,
        *,
        data=None,
        files=None,
        json=None,
        content=None,
        params=None,
        headers=None,
        timeout=None,
    ) -> httpx.Response:
        if self._autorefresh_tokens:
            return await self._autorefresh_token_request(
                method,
                path,
                data=data,
                files=files,
                json=json,
                content=content,
                params=params,
                headers=headers,
                timeout=timeout,
            )
        return await self._request(
            method,
            path,
            data=data,
            files=files,
            json=json,
            content=content,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    async def _request(  # type: ignore[no-untyped-def]
        self,
        method: str,
        path: str,
        *,
        data=None,
        files=None,
        json=None,
        content=None,
        params=None,
        headers=None,
        timeout=None,
    ) -> httpx.Response:
        headers = headers or {}
        headers.update(await self._token_proxy.get_auth_header())
        async with self.http_client as client:
            response = await client.request(
                method,
                path,
                data=data,
                files=files,
                json=json,
                content=content,
                params=params,
                headers=headers,
                timeout=timeout,
            )

        return response

    async def _run_token_refresh(self) -> None:
        # Why do we have to check if token was changed?
        # Consider the situation:
        # * we send 4 requests at the same time
        # * 3 of the 4 are returned with 401 token_expired errors
        # * 1 of the 4 is still waiting for response
        #   (any reasons, may be rate limit at API server side)
        # * one of failed 3 requests have refreshed the token,
        #   the rest of the 3 will use the refreshed token for retries
        # * the waiting request have got 401 token_expired response.
        #   But the token has been just refreshed, so there is no need to refresh it again.
        #   To track this case we have to check if the token has been updated
        #   (since last get_auth_header call).
        #   If token has been updated, then we just need to retry original request with a
        #   refreshed auth data.
        if await self._token_proxy.is_updated():
            return
        if not await self._token_proxy.lock_for_update():
            return
        try:
            refresh_data = await self._token_proxy.get_refresh_data()
            async with self.http_client as client:
                response = await client.post("/token/refresh", json=refresh_data)
            await self._token_proxy.update(response.json())
        finally:
            await self._token_proxy.release_lock()

    async def _autorefresh_token_request(self, *args: str, **kwargs: str) -> httpx.Response:
        try:
            response = await self._request(*args, **kwargs)
            return response
        except (TokenExpiredError, InvalidAccessTokenError):
            await self._run_token_refresh()
            response = await self._request(*args, **kwargs)
            return response
