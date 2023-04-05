import respx
import pytest
import asyncio

from tests.fixtures.huntflow import TokenTypes
from huntflow_api_client.errors import InvalidAccessTokenError, TokenExpiredError


@respx.mock
async def test_valid_access_token__ok(
    fake_huntflow,
    huntflow_api_factory,
):
    huntflow_api = huntflow_api_factory()

    token = await huntflow_api._token_proxy._storage.get()
    fake_huntflow.add_token(token.access_token)

    response = await huntflow_api.request("GET", "/ping")

    assert response.status_code == 200
    assert fake_huntflow.ping_route.called


@pytest.mark.parametrize(
    ("unauthorized_token_type", "authorization_error"),
    [
        (TokenTypes.INVALID_TOKEN, InvalidAccessTokenError),
        (TokenTypes.EXPIRED_TOKEN, TokenExpiredError),
    ],
)
@respx.mock
async def test_authorization_error__error(
    fake_huntflow,
    huntflow_api_factory,
    unauthorized_token_type,
    authorization_error,
):
    huntflow_api = huntflow_api_factory()

    token = await huntflow_api._token_proxy._storage.get()
    fake_huntflow.add_token(token.access_token, unauthorized_token_type)

    with pytest.raises(authorization_error):
        await huntflow_api.request("GET", "/ping")

    assert fake_huntflow.ping_route.call_count == 1
    assert fake_huntflow.ping_route.calls.last.response.status_code == 401

    assert fake_huntflow.token_refresh_route.call_count == 0


@pytest.mark.parametrize(
    "unauthorized_token_type",
    (TokenTypes.INVALID_TOKEN, TokenTypes.EXPIRED_TOKEN),
)
@respx.mock
async def test_auto_refresh_tokens__ok(
    fake_huntflow,
    huntflow_api_factory,
    unauthorized_token_type,
):
    huntflow_api = huntflow_api_factory(auto_refresh_tokens=True)

    token = await huntflow_api._token_proxy._storage.get()
    fake_huntflow.add_token(token.access_token, unauthorized_token_type)

    await huntflow_api.request("GET", "/ping")

    assert fake_huntflow.ping_route.call_count == 2
    assert fake_huntflow.ping_route.calls[0].response.status_code == 401
    assert fake_huntflow.ping_route.calls[1].response.status_code == 200

    assert fake_huntflow.token_refresh_route.call_count == 1


@pytest.mark.parametrize(
    "unauthorized_token_type",
    (TokenTypes.INVALID_TOKEN, TokenTypes.EXPIRED_TOKEN),
)
@respx.mock
async def test_auto_refresh_tokens_simultaneous_requests__ok(
    fake_huntflow,
    huntflow_api_factory,
    unauthorized_token_type,
):
    async def make_request():
        await huntflow_api.request("GET", "/ping")

    huntflow_api = huntflow_api_factory(auto_refresh_tokens=True)

    token = await huntflow_api._token_proxy._storage.get()
    fake_huntflow.add_token(token.access_token, unauthorized_token_type)

    calls = [make_request() for _ in range(2)]

    await asyncio.gather(*calls)

    assert fake_huntflow.ping_route.call_count > 1
    assert fake_huntflow.ping_route.calls.last.response.status_code == 200

    assert fake_huntflow.token_refresh_route.call_count == 1
