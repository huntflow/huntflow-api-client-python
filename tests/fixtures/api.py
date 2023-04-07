import pytest

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens import ApiToken

API_TOKEN = ApiToken("mocked token")


@pytest.fixture()
def api_url() -> str:
    return "https://api.huntflow.dev/v2"


@pytest.fixture
def api_client(api_url: str) -> HuntflowAPI:
    api_client = HuntflowAPI(base_url=api_url, token=API_TOKEN)
    return api_client
