import pathlib
import json

import pytest

from huntflow_api_client_python.api import HuntflowApi


API_URL = "http://mocked.url"
API_TOKEN = "mocked token"


def read_json(file_path: str):
    return json.loads(read_file(file_path))


def read_file(file_path: str, mode: str = "r"):
    data_dir = pathlib.Path(__file__).parent.joinpath("data")
    path = data_dir / file_path
    with open(path, mode) as f:
        return f.read()


@pytest.fixture
def api_client():
    api_client = HuntflowApi(
        base_url=API_URL,
        token=API_TOKEN,
    )
    return api_client
