import pytest

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens import ApiToken

API_URL = "https://api.huntflow.dev/v2"
API_TOKEN = ApiToken("mocked token")

ACCESS_TOKEN_EXPIRES_IN = 86400 * 7
REFRESH_TOKEN_EXPIRES_IN = 86400 * 14


@pytest.fixture
def api_client() -> HuntflowAPI:
    api_client = HuntflowAPI(base_url=API_URL, token=API_TOKEN)
    return api_client


pytest_plugins = [
    "tests.fixtures.api",
    "tests.fixtures.huntflow",
    "tests.fixtures.token_proxy",
    "tests.fixtures.tokens",
]
