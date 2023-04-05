import pytest
from typing import Callable

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens import ApiToken
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy


@pytest.fixture()
def huntflow_api_url() -> str:
    return "https://api.huntflow.dev/v2"


@pytest.fixture
def api_client(huntflow_api_url: str, api_token: ApiToken) -> HuntflowAPI:
    api_client = HuntflowAPI(base_url=huntflow_api_url, token=api_token)
    return api_client


@pytest.fixture()
def huntflow_api_factory(
    huntflow_api_url: str,
    huntflow_token_proxy: HuntflowTokenProxy,
) -> Callable[[bool], HuntflowAPI]:
    def create(auto_refresh_tokens: bool = False) -> HuntflowAPI:
        return HuntflowAPI(
            base_url=huntflow_api_url,
            token_proxy=huntflow_token_proxy,
            auto_refresh_tokens=auto_refresh_tokens,
        )

    return create
