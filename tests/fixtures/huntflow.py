import httpx
import respx
import pytest
import re
import uuid
import enum

from typing import Dict
from collections import defaultdict

from ..conftest import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN


class TokenTypes(enum.Enum):
    EXPIRED_TOKEN = 0
    INVALID_TOKEN = 1
    VALID_TOKEN = 2


class Huntflow:
    def __init__(self, base_url: str):
        self.base_url = base_url

        self.token_refresh_matcher = re.compile(f"{self.base_url}/token/refresh")
        self.ping_matcher = re.compile(f"{self.base_url}/ping")

        self.token_refresh_route = respx.post(self.token_refresh_matcher).mock(
            side_effect=self.token_refresh,
        )
        self.ping_route = respx.get(self.ping_matcher).mock(side_effect=self.ping)

        self.tokens: Dict[TokenTypes, list] = defaultdict(list)

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

    def token_refresh(self, _: httpx.Request) -> httpx.Response:
        access_token = uuid.uuid4().hex
        self.add_token(access_token)
        return httpx.Response(
            status_code=200,
            json={
                "access_token": access_token,
                "token_type": "test_token_type",
                "expires_in": ACCESS_TOKEN_EXPIRES_IN,
                "refresh_token_expires_in": REFRESH_TOKEN_EXPIRES_IN,
                "refresh_token": uuid.uuid4().hex,
            },
        )

    def ping(self, request: httpx.Request) -> httpx.Response:
        *_, access_token = request.headers["Authorization"].split()

        if access_token in self.tokens[TokenTypes.VALID_TOKEN]:
            return self.access_token_is_valid(request)
        elif access_token in self.tokens[TokenTypes.INVALID_TOKEN]:
            return self.access_token_is_invalid(request)
        elif access_token in self.tokens[TokenTypes.EXPIRED_TOKEN]:
            return self.access_token_is_expired(request)
        else:
            raise NotImplementedError

    def add_token(self, token: str, token_type: TokenTypes = TokenTypes.VALID_TOKEN):
        self.tokens[token_type].append(token)


@pytest.fixture()
def fake_huntflow(huntflow_api_url) -> Huntflow:
    return Huntflow(base_url=huntflow_api_url)
