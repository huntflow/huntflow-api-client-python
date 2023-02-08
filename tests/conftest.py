import pytest

from huntflow_api_client import HuntflowAPI


API_URL = "http://mocked.url"
API_TOKEN = "mocked token"


@pytest.fixture
def api_client():
    api_client = HuntflowAPI(
        base_url=API_URL,
        token=API_TOKEN,
    )
    return api_client
