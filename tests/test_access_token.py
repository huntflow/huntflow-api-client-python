import asyncio
from typing import Callable, Type, Union

import pytest
import respx

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.errors import InvalidAccessTokenError, TokenExpiredError
from tests.fixtures.huntflow import Huntflow, TokenTypes


@respx.mock
async def test_valid_access_token__ok(
    fake_huntflow: Huntflow,
    huntflow_api_factory: Callable[[bool], HuntflowAPI],
) -> None:
    huntflow_api = huntflow_api_factory(False)

    token = await huntflow_api._token_proxy._storage.get()  # type: ignore[attr-defined]
    fake_huntflow.add_token(token.access_token)

    response = await huntflow_api.request("GET", "/me")

    assert response.status_code == 200
    assert fake_huntflow.me_route.called


@pytest.mark.parametrize(
    ("unauthorized_token_type", "authorization_error"),
    [
        (TokenTypes.INVALID_TOKEN, InvalidAccessTokenError),
        (TokenTypes.EXPIRED_TOKEN, TokenExpiredError),
    ],
)
@respx.mock
async def test_authorization_error__error(
    fake_huntflow: Huntflow,
    huntflow_api_factory: Callable[[bool], HuntflowAPI],
    unauthorized_token_type: TokenTypes,
    authorization_error: Union[Type[InvalidAccessTokenError], Type[TokenExpiredError]],
) -> None:
    huntflow_api = huntflow_api_factory(False)

    token = await huntflow_api._token_proxy._storage.get()  # type: ignore[attr-defined]
    fake_huntflow.add_token(token.access_token, unauthorized_token_type)

    with pytest.raises(authorization_error):
        await huntflow_api.request("GET", "/me")

    assert fake_huntflow.me_route.call_count == 1
    assert fake_huntflow.me_route.calls.last.response.status_code == 401

    assert fake_huntflow.token_refresh_route.call_count == 0


@pytest.mark.parametrize(
    "unauthorized_token_type",
    (TokenTypes.INVALID_TOKEN, TokenTypes.EXPIRED_TOKEN),
)
@respx.mock
async def test_auto_refresh_tokens__ok(
    fake_huntflow: Huntflow,
    huntflow_api_factory: Callable[[bool], HuntflowAPI],
    unauthorized_token_type: TokenTypes,
) -> None:
    huntflow_api = huntflow_api_factory(True)

    token = await huntflow_api._token_proxy._storage.get()  # type: ignore[attr-defined]
    fake_huntflow.add_token(token.access_token, unauthorized_token_type)

    await huntflow_api.request("GET", "/me")

    assert fake_huntflow.me_route.call_count == 2
    assert fake_huntflow.me_route.calls[0].response.status_code == 401
    assert fake_huntflow.me_route.calls[1].response.status_code == 200

    assert fake_huntflow.token_refresh_route.call_count == 1


@pytest.mark.parametrize(
    "unauthorized_token_type",
    (TokenTypes.INVALID_TOKEN, TokenTypes.EXPIRED_TOKEN),
)
@respx.mock
async def test_auto_refresh_tokens_simultaneous_requests__ok(
    fake_huntflow: Huntflow,
    huntflow_api_factory: Callable[[bool], HuntflowAPI],
    unauthorized_token_type: TokenTypes,
) -> None:
    huntflow_api = huntflow_api_factory(True)

    token = await huntflow_api._token_proxy._storage.get()  # type: ignore[attr-defined]
    fake_huntflow.add_token(token.access_token, unauthorized_token_type)

    calls = [huntflow_api.request("GET", "/me") for _ in range(4)]

    responses = await asyncio.gather(*calls)

    assert fake_huntflow.me_route.call_count > 1

    assert all(response.status_code == 200 for response in responses)
    assert fake_huntflow.token_refresh_route.call_count == 1
