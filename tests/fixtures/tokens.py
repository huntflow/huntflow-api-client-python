import json
import pathlib
import time
import uuid
from typing import Any, Dict, Generator

import pytest

from huntflow_api_client.tokens import ApiToken

TOKEN_FILE_PATH = pathlib.Path(__file__).parent.resolve()
ACCESS_TOKEN_EXPIRES_IN = 86400 * 7
REFRESH_TOKEN_EXPIRES_IN = 86400 * 14


@pytest.fixture()
def api_token() -> ApiToken:
    return ApiToken("mocked token")


@pytest.fixture()
def access_token_expires_in() -> int:
    return ACCESS_TOKEN_EXPIRES_IN


@pytest.fixture()
def refresh_token_expires_in() -> int:
    return REFRESH_TOKEN_EXPIRES_IN


@pytest.fixture()
def token_data(access_token_expires_in: int) -> Dict[str, Any]:
    now = time.time()
    return {
        "access_token": uuid.uuid4().hex,
        "refresh_token": uuid.uuid4().hex,
        "expiration_timestamp": now + access_token_expires_in,
        "last_refresh_timestamp": now,
    }


@pytest.fixture()
def refresh_token_data(
    access_token_expires_in: int,
    refresh_token_expires_in: int,
) -> Dict[str, Any]:
    return {
        "access_token": uuid.uuid4().hex,
        "token_type": "token_type",
        "expires_in": access_token_expires_in,
        "refresh_token_expires_in": refresh_token_expires_in,
        "refresh_token": uuid.uuid4().hex,
    }


@pytest.fixture()
def token_storage_filename() -> str:
    return f"{TOKEN_FILE_PATH}/test_token.json"


@pytest.fixture()
def token_file_storage(
    token_storage_filename: str,
    token_data: Dict[str, Any],
) -> Generator[str, None, None]:
    data = token_data
    with open(token_storage_filename, "w") as f:
        json.dump(data, f)

    yield f.name

    pathlib.Path.unlink(pathlib.Path(f.name))
