import re
import json
from typing import Dict, Optional

import httpx
import pytest
import respx

from tests.fixtures.tokens import TokenPair, get_token_refresh_data


BASE_URL = "https://api.huntflow.dev/v2"


class HuntflowServer:
    base_url = BASE_URL
    token_pair: TokenPair
    is_expired_token: bool

    def __init__(self, token_pair: Optional[TokenPair] = None):
        self.token_pair = token_pair or TokenPair()
        self.is_expired_token = False

        self.token_refresh_matcher = re.compile(f"{self.base_url}/token/refresh")
        self.me_matcher = re.compile(f"{self.base_url}/me")

        self.token_refresh_route = respx.post(self.token_refresh_matcher).mock(
            side_effect=self.token_refresh,
        )
        self.me_route = respx.get(self.me_matcher).mock(side_effect=self.me)

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

    def token_refresh(self, request: httpx.Request) -> httpx.Response:
        if not self.is_expired_token:
            return httpx.Response(400)
        request_data = json.loads(request.content)
        refresh_token = request_data["refresh_token"]
        assert refresh_token == self.token_pair.refresh_token

        self.token_pair = TokenPair()
        self.is_expired_token = False
        return httpx.Response(
            status_code=200,
            json=get_token_refresh_data(self.token_pair),
        )

    def me(self, request: httpx.Request) -> httpx.Response:
        *_, access_token = request.headers["Authorization"].split()

        if access_token == self.token_pair.access_token:
            if self.is_expired_token:
                return self.access_token_is_expired(request)
            return self.access_token_is_valid(request)
        return self.access_token_is_invalid(request)

    def expire_token(self):
        self.is_expired_token = True

    def set_token_pair(self, token_pair: TokenPair):
        self.token_pair = token_pair
        self.is_expired_token = False


@pytest.fixture()
def fake_huntflow(token_pair) -> HuntflowServer:
    return HuntflowServer(token_pair)
