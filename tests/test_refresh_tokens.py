import pytest
from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.api import ApiTokens
from huntflow_api_client.entities.tags import AccountTag
from huntflow_api_client.event_hooks.response import raise_token_expired_hook
from huntflow_api_client.models.response.tags import AccountTagResponse

pytestmark = pytest.mark.asyncio

api_url = "https://api.huntflow.ru"
access_token = "at"
refresh_token = "rt"
refresh_token_url = f"{api_url}/v2/token/refresh"
token_expired_response = {"errors": [{"title": "Authorization Error", "detail": "token_expired"}]}
refresh_token_response = {"access_token": "new_access", "refresh_token": "new_refresh"}
account_tag_response = {"id": 1, "name": "Blacklist", "color": "00ad3b"}


async def test_run_refresh_token_value_error():
    api_client = HuntflowAPI(base_url=api_url, access_token=access_token)
    with pytest.raises(ValueError) as err:
        await api_client.run_token_refresh()

    assert err.match("Refresh token is required.")


async def test_run_refresh_token_stored_in_the_api(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=refresh_token_url,
        json=refresh_token_response,
        match_content=b'{"refresh_token": "rt"}'
    )
    api_client = HuntflowAPI(
        base_url=api_url, access_token=access_token, refresh_token=refresh_token,
    )
    assert api_client.access_token == access_token
    assert api_client.refresh_token == refresh_token

    await api_client.run_token_refresh()

    assert api_client.access_token == refresh_token_response["access_token"]
    assert api_client.refresh_token == refresh_token_response["refresh_token"]


async def test_run_refresh_token_passed_to_the_method(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=refresh_token_url,
        json=refresh_token_response,
        match_content=b'{"refresh_token": "rt"}'
    )
    api_client = HuntflowAPI(base_url=api_url, access_token=access_token)
    assert api_client.access_token == access_token
    assert api_client.refresh_token is None

    await api_client.run_token_refresh(refresh_token=refresh_token)

    assert api_client.access_token == refresh_token_response["access_token"]
    assert api_client.refresh_token == refresh_token_response["refresh_token"]


async def test_run_refresh_token_callbacks(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=refresh_token_url,
        json=refresh_token_response,
        match_content=b'{"refresh_token": "rt"}'
    )
    callback_kwargs = []

    async def pre_cb(tokens_for_refresh):
        callback_kwargs.append(tokens_for_refresh)

    async def post_cb(old_tokens, new_tokens):
        callback_kwargs.append((old_tokens, new_tokens))

    api_client = HuntflowAPI(base_url=api_url, access_token=access_token)
    assert api_client.access_token == access_token
    assert api_client.refresh_token is None

    old_tokens = ApiTokens(access_token=access_token, refresh_token=refresh_token)
    new_tokens = await api_client.run_token_refresh(
        refresh_token=refresh_token, pre_cb=pre_cb, post_cb=post_cb,
    )

    assert api_client.access_token == refresh_token_response["access_token"]
    assert api_client.refresh_token == refresh_token_response["refresh_token"]
    assert callback_kwargs == [old_tokens, (old_tokens, new_tokens)]


async def test_auto_refresh_tokens_error():
    with pytest.raises(ValueError) as err:
        HuntflowAPI(base_url=api_url, access_token=access_token, auto_refresh_tokens=True)

    assert err.match("Refresh token is required.")


async def test_auto_refresh_tokens(httpx_mock: HTTPXMock):
    account_id = 1
    tag_id = 1
    httpx_mock.add_response(  # Token expired
        status_code=401,
        url=f"{api_url}/v2/accounts/{account_id}/tags/{tag_id}",
        match_headers={"Authorization": f"Bearer {access_token}"},
        json=token_expired_response,
    )
    httpx_mock.add_response(  # Refresh token
        url=refresh_token_url,
        json=refresh_token_response,
        match_content=b'{"refresh_token": "rt"}'
    )
    httpx_mock.add_response(  # Success result
        status_code=200,
        url=f"{api_url}/v2/accounts/{account_id}/tags/{tag_id}",
        match_headers={"Authorization": f"Bearer {refresh_token_response['access_token']}"},
        json=account_tag_response,
    )

    callback_kwargs = []

    async def pre_cb(old_tokens):
        callback_kwargs.append(old_tokens)

    async def post_cb(old_tokens, new_tokens):
        callback_kwargs.append((old_tokens, new_tokens))

    api_client = HuntflowAPI(
        base_url=api_url,
        access_token=access_token,
        refresh_token=refresh_token,
        auto_refresh_tokens=True,
        pre_refresh_cb=pre_cb,
        post_refresh_cb=post_cb,
    )

    assert api_client.access_token == access_token
    assert api_client.refresh_token == refresh_token
    assert raise_token_expired_hook in api_client._response_event_hooks

    tags = AccountTag(api_client)
    response = await tags.get(account_id, tag_id)

    assert response == AccountTagResponse(**account_tag_response)
    assert api_client.access_token == refresh_token_response["access_token"]
    assert api_client.refresh_token == refresh_token_response["refresh_token"]
    old_tokens = ApiTokens(access_token=access_token, refresh_token=refresh_token)
    new_tokens = ApiTokens(**refresh_token_response)
    assert callback_kwargs == [old_tokens, (old_tokens, new_tokens)]
