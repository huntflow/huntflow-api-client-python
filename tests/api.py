import json
import uuid
from typing import Any, Callable, Dict, Optional

import httpx
import respx
from respx.types import URLPatternTypes

from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage

BASE_URL = "https://api.huntflow.dev/v2"
ACCESS_TOKEN_EXPIRES_IN = 86400 * 7
REFRESH_TOKEN_EXPIRES_IN = 86400 * 14


class TokenPair:
    def __init__(self, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        self.access_token = access_token or uuid.uuid4().hex
        self.refresh_token = refresh_token or uuid.uuid4().hex


class Router:
    _api: "FakeAPIServer"

    def __init__(self, method: str, url: URLPatternTypes, name: Optional[str] = None):
        self.method = method
        self.url = url
        self.name = name or str(url)

    @classmethod
    def register_api(cls, api: "FakeAPIServer") -> None:
        cls._api = api

    def __call__(self, api_handler: Callable) -> Callable:
        def inner(*args: Any, **kwargs: Any) -> Any:
            return api_handler(self._api, *args, **kwargs)

        respx.request(
            method=self.method,
            url=f"{BASE_URL}{self.url}",
            name=self.name,
        ).mock(side_effect=inner)

        return inner


class FakeAPIServer:
    base_url = BASE_URL
    token_pair: TokenPair
    is_expired_token: bool

    def __init__(self, token_pair: Optional[TokenPair] = None):
        self.token_pair = token_pair or TokenPair()
        self.is_expired_token = False
        Router.register_api(self)

    @classmethod
    def access_token_is_valid(cls, _: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    @classmethod
    def access_token_is_expired(cls, _: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=401,
            json={
                "errors": [
                    {
                        "type": "authorization_error",
                        "title": "Authorization Error",
                        "detail": "token_expired",
                    },
                ],
            },
        )

    @classmethod
    def access_token_is_invalid(cls, _: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=401,
            json={
                "errors": [
                    {
                        "type": "authorization_error",
                        "title": "Authorization Error",
                        "detail": "Invalid access token",
                    },
                ],
            },
        )

    @Router("POST", "/token/refresh")
    def token_refresh(self, request: httpx.Request) -> httpx.Response:
        if not self.is_expired_token:
            return httpx.Response(400)
        request_data = json.loads(request.content)
        refresh_token = request_data["refresh_token"]
        if refresh_token != self.token_pair.refresh_token:
            return httpx.Response(
                404,
                json={
                    "errors": [
                        {
                            "type": "not_found",
                            "title": "error.robot_token.not_found",
                        },
                    ],
                },
            )

        self.token_pair = TokenPair()
        self.is_expired_token = False
        return httpx.Response(
            status_code=200,
            json=get_token_refresh_data(self.token_pair),
        )

    @Router("GET", "/me")
    def me(self, request: httpx.Request) -> httpx.Response:
        *_, access_token = request.headers["Authorization"].split()

        if access_token == self.token_pair.access_token:
            if self.is_expired_token:
                return self.access_token_is_expired(request)
            return self.access_token_is_valid(request)
        return self.access_token_is_invalid(request)

    def expire_token(self) -> None:
        self.is_expired_token = True

    def set_token_pair(self, token_pair: TokenPair) -> None:
        self.token_pair = token_pair
        self.is_expired_token = False


def new_token_storage(file_name: str, token_pair: TokenPair) -> HuntflowTokenFileStorage:
    token_data = {
        "access_token": token_pair.access_token,
        "refresh_token": token_pair.refresh_token,
    }
    with open(file_name, "w") as fout:
        json.dump(token_data, fout)
    storage = HuntflowTokenFileStorage(file_name)
    return storage


def get_token_refresh_data(token_pair: TokenPair) -> Dict[str, Any]:
    return {
        "access_token": token_pair.access_token,
        "expires_in": ACCESS_TOKEN_EXPIRES_IN,
        "refresh_token_expires_in": REFRESH_TOKEN_EXPIRES_IN,
        "refresh_token": token_pair.refresh_token,
    }
