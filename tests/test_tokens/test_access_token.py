import asyncio
import json

import pytest
import respx

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.errors.errors import (
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
    TokenExpiredError,
)
from huntflow_api_client.tokens.locker import AsyncioLockLocker
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage
from tests.api import FakeAPIServer, TokenPair


@respx.mock
async def test_valid_access_token__ok(
    fake_server: FakeAPIServer,
    token_proxy: HuntflowTokenProxy,
) -> None:
    api = HuntflowAPI(
        fake_server.base_url,
        token_proxy=token_proxy,
        auto_refresh_tokens=True,
    )

    response = await api.request("GET", "/me")

    assert response.status_code == 200
    assert respx.routes["/me"].called


@respx.mock
async def test_access_token_invalid__error(
    fake_server: FakeAPIServer,
    token_proxy: HuntflowTokenProxy,
) -> None:
    huntflow_api = HuntflowAPI(
        fake_server.base_url,
        token_proxy=token_proxy,
        auto_refresh_tokens=False,
    )
    fake_server.set_token_pair(TokenPair())

    with pytest.raises(InvalidAccessTokenError):
        await huntflow_api.request("GET", "/me")

    assert respx.routes["/me"].call_count == 1
    assert respx.routes["/me"].calls.last.response.status_code == 401

    assert respx.routes["/token/refresh"].call_count == 0


@respx.mock
async def test_access_token_expired__error(
    fake_server: FakeAPIServer,
    token_proxy: HuntflowTokenProxy,
) -> None:
    huntflow_api = HuntflowAPI(
        fake_server.base_url,
        token_proxy=token_proxy,
        auto_refresh_tokens=False,
    )
    fake_server.expire_token()

    with pytest.raises(TokenExpiredError):
        await huntflow_api.request("GET", "/me")

    assert respx.routes["/me"].call_count == 1
    assert respx.routes["/me"].calls.last.response.status_code == 401

    assert respx.routes["/token/refresh"].call_count == 0


@respx.mock
async def test_invalid_refresh_token__error(
    fake_server: FakeAPIServer,
    token_proxy: HuntflowTokenProxy,
) -> None:
    huntflow_api = HuntflowAPI(
        fake_server.base_url,
        token_proxy=token_proxy,
        auto_refresh_tokens=True,
    )
    fake_server.set_token_pair(
        TokenPair(
            access_token=fake_server.token_pair.access_token,
            refresh_token="1",
        ),
    )
    fake_server.expire_token()

    with pytest.raises(InvalidRefreshTokenError):
        await huntflow_api.request("GET", "/me")

    assert respx.routes["/me"].call_count == 1
    assert respx.routes["/me"].calls.last.response.status_code == 401

    assert respx.routes["/token/refresh"].call_count == 1


@respx.mock
async def test_auto_refresh_tokens__ok(
    fake_server: FakeAPIServer,
    token_proxy: HuntflowTokenProxy,
) -> None:
    huntflow_api = HuntflowAPI(
        fake_server.base_url,
        token_proxy=token_proxy,
        auto_refresh_tokens=True,
    )
    fake_server.expire_token()

    await huntflow_api.request("GET", "/me")

    assert respx.routes["/me"].call_count == 2
    assert respx.routes["/me"].calls[0].response.status_code == 401
    assert respx.routes["/me"].calls[1].response.status_code == 200

    assert respx.routes["/token/refresh"].call_count == 1
    assert fake_server.is_expired_token is False


@respx.mock
async def test_auto_refresh_tokens_several_api_one_proxy__ok(
    fake_server: FakeAPIServer,
    token_proxy: HuntflowTokenProxy,
) -> None:
    api_count = 10
    apis = [
        HuntflowAPI(
            fake_server.base_url,
            token_proxy=token_proxy,
            auto_refresh_tokens=True,
        )
        for _ in range(api_count)
    ]
    fake_server.expire_token()

    calls = [api.request("GET", "/me") for api in apis]

    responses = await asyncio.gather(*calls)

    # Why api_count * 2? Every first call will fail because of expired token,
    # after refreshing there will be exactly one retry for the failed requests
    assert respx.routes["/me"].call_count == api_count * 2

    assert all(response.status_code == 200 for response in responses)
    assert respx.routes["/token/refresh"].call_count == 1
    assert fake_server.is_expired_token is False


@respx.mock
async def test_auto_refresh_tokens_several_api_several_proxies__ok(
    fake_server: FakeAPIServer,
    token_filename: str,
    token_pair: TokenPair,
) -> None:
    # note: there must be the same locker across different proxies
    locker = AsyncioLockLocker()

    token_data = {
        "access_token": token_pair.access_token,
        "refresh_token": token_pair.refresh_token,
    }
    with open(token_filename, "w") as fout:
        json.dump(token_data, fout)

    api_count = 10
    apis = []
    for _ in range(api_count):
        storage = HuntflowTokenFileStorage(token_filename)
        token_proxy = HuntflowTokenProxy(storage, locker)
        api = HuntflowAPI(fake_server.base_url, token_proxy=token_proxy, auto_refresh_tokens=True)
        apis.append(api)

    fake_server.expire_token()

    calls = [api.request("GET", "/me") for api in apis]

    responses = await asyncio.gather(*calls)

    # Why api_count * 2? Every first call will fail because of expired token,
    # after refreshing there will be exactly one retry for the failed requests
    assert respx.routes["/me"].call_count == api_count * 2

    assert all(response.status_code == 200 for response in responses)
    assert respx.routes["/token/refresh"].call_count == 1
    assert fake_server.is_expired_token is False
