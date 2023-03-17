import pytest

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens import ApiToken


API_URL = "https://api.huntflow.dev/v2"
API_TOKEN = ApiToken("mocked token")


@pytest.fixture
def api_client():
    api_client = HuntflowAPI(base_url=API_URL, token=API_TOKEN)
    return api_client
