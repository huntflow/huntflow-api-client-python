import asyncio
from pathlib import Path
from typing import Type, Union

import pytest
import respx

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.errors import InvalidAccessTokenError, TokenExpiredError
from tests.fixtures.huntflow import Huntflow, TokenTypes

from .helpers import get_huntflow_token_proxy, get_token_data


@respx.mock
async def test_valid_access_token__ok(
    huntflow: Huntflow,
    tmp_path: Path,
) -> None:
    proxy, storage = get_huntflow_token_proxy(tmp_path)
    api = HuntflowAPI(token_proxy=proxy)

    api_token = get_token_data(storage)
    huntflow.add_token(api_token["access_token"], TokenTypes.VALID_TOKEN)

    response = await api.request("GET", "/me")

    assert response.status_code == 200
    assert huntflow.me_route.called


@pytest.mark.parametrize(
    ("unauthorized_token_type", "authorization_error"),
    [
        (TokenTypes.INVALID_TOKEN, InvalidAccessTokenError),
        (TokenTypes.EXPIRED_TOKEN, TokenExpiredError),
    ],
)
@respx.mock
async def test_access_token_invalid_or_expired__authorization_error(
    huntflow: Huntflow,
    tmp_path: Path,
    unauthorized_token_type: TokenTypes,
    authorization_error: Union[Type[InvalidAccessTokenError], Type[TokenExpiredError]],
) -> None:
    proxy, storage = get_huntflow_token_proxy(tmp_path)
    api = HuntflowAPI(token_proxy=proxy)

    api_token = get_token_data(storage)
    huntflow.add_token(api_token["access_token"], unauthorized_token_type)

    with pytest.raises(authorization_error):
        await api.request("GET", "/me")

    assert huntflow.me_route.call_count == 1
    assert huntflow.me_route.calls.last.response.status_code == 401

    assert huntflow.token_refresh_route.call_count == 0


@pytest.mark.parametrize(
    "unauthorized_token_type",
    (TokenTypes.INVALID_TOKEN, TokenTypes.EXPIRED_TOKEN),
)
@respx.mock
async def test_auto_refresh_tokens__ok(
    huntflow: Huntflow,
    tmp_path: Path,
    unauthorized_token_type: TokenTypes,
) -> None:
    proxy, storage = get_huntflow_token_proxy(tmp_path)
    api = HuntflowAPI(token_proxy=proxy, auto_refresh_tokens=True)

    api_token = get_token_data(storage)
    huntflow.add_token(api_token["access_token"], unauthorized_token_type)

    await api.request("GET", "/me")

    assert huntflow.me_route.call_count == 2
    assert huntflow.me_route.calls[0].response.status_code == 401
    assert huntflow.me_route.calls[1].response.status_code == 200

    assert huntflow.token_refresh_route.call_count == 1


@pytest.mark.parametrize(
    "unauthorized_token_type",
    (TokenTypes.INVALID_TOKEN, TokenTypes.EXPIRED_TOKEN),
)
@respx.mock
async def test_auto_refresh_tokens_simultaneous_requests__ok(
    huntflow: Huntflow,
    tmp_path: Path,
    unauthorized_token_type: TokenTypes,
) -> None:
    proxy, storage = get_huntflow_token_proxy(tmp_path)
    api = HuntflowAPI(token_proxy=proxy, auto_refresh_tokens=True)

    api_token = get_token_data(storage)
    huntflow.add_token(api_token["access_token"], unauthorized_token_type)

    requests = [api.request("GET", "/me") for _ in range(4)]

    responses = await asyncio.gather(*requests)

    assert huntflow.me_route.call_count > 1

    assert all(response.status_code == 200 for response in responses)
    assert huntflow.token_refresh_route.call_count == 1
