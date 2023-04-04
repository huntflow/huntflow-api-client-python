import pytest

from huntflow_api_client import HuntflowAPI


@pytest.fixture()
def huntflow_api_url() -> str:
    return "https://api.huntflow.dev/v2"


@pytest.fixture()
def huntflow_api_factory(huntflow_api_url, huntflow_token_proxy):
    def create(auto_refresh_tokens: bool = False) -> HuntflowAPI:
        return HuntflowAPI(
            base_url=huntflow_api_url,
            token_proxy=huntflow_token_proxy,
            auto_refresh_tokens=auto_refresh_tokens,
        )

    return create
