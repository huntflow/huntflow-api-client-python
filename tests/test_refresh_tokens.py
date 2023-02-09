import pytest
from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI

pytestmark = pytest.mark.asyncio

API_URL = "http://mocked.url"
ACCESS_TOKEN = "mocked token"
REFRESH_TOKEN = "mocked refresh token"


async def test_run_refresh_token_value_error():
    api_client = HuntflowAPI(base_url=API_URL, access_token=ACCESS_TOKEN)
    with pytest.raises(ValueError):
        await api_client.run_token_refresh()


async def test_run_refresh_token_from_api_instance(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/token/refresh",
        json={"access_token": "at", "refresh_token": "rt"},
        match_content=b'{"refresh_token": "mocked refresh token"}'
    )
    api_client = HuntflowAPI(
        base_url=API_URL, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN,
    )
    assert api_client.access_token == ACCESS_TOKEN
    assert api_client.refresh_token == REFRESH_TOKEN

    await api_client.run_token_refresh()

    assert api_client.access_token == "at"
    assert api_client.refresh_token == "rt"


async def test_run_refresh_token_from_method(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/token/refresh",
        json={"access_token": "at", "refresh_token": "rt"},
        match_content=b'{"refresh_token": "mocked refresh token"}'
    )
    api_client = HuntflowAPI(base_url=API_URL, access_token=ACCESS_TOKEN)
    assert api_client.access_token == ACCESS_TOKEN
    assert api_client.refresh_token is None

    await api_client.run_token_refresh(refresh_token=REFRESH_TOKEN)

    assert api_client.access_token == "at"
    assert api_client.refresh_token == "rt"


async def test_run_refresh_token_callbacks(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{API_URL}/v2/token/refresh",
        json={"access_token": "at", "refresh_token": "rt"},
        match_content=b'{"refresh_token": "mocked refresh token"}'
    )
    callback_args = []

    async def pre_cb(*args):
        callback_args.append(args)

    async def post_cb(*args):
        callback_args.append(args)

    api_client = HuntflowAPI(base_url=API_URL, access_token=ACCESS_TOKEN)
    assert api_client.access_token == ACCESS_TOKEN
    assert api_client.refresh_token is None

    tokens = await api_client.run_token_refresh(
        refresh_token=REFRESH_TOKEN, pre_cb=pre_cb, post_cb=post_cb,
    )

    assert api_client.access_token == "at"
    assert api_client.refresh_token == "rt"
    assert callback_args == [(REFRESH_TOKEN,), (tokens,)]
