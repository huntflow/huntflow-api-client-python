import json
import uuid
import pathlib
import time

import pytest

from ..conftest import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN


TOKEN_FILE_PATH = pathlib.Path(__file__).parent.resolve()


@pytest.fixture()
def access_token_expires_in():
    return ACCESS_TOKEN_EXPIRES_IN


@pytest.fixture()
def refresh_token_expires_in():
    return REFRESH_TOKEN_EXPIRES_IN


@pytest.fixture()
def token_data(access_token_expires_in):
    now = time.time()
    return {
        "access_token": uuid.uuid4().hex,
        "refresh_token": uuid.uuid4().hex,
        "expiration_timestamp": now + access_token_expires_in,
        "last_refresh_timestamp": now,
    }


@pytest.fixture()
def refresh_token_data(access_token_expires_in, refresh_token_expires_in):
    return {
        "access_token": uuid.uuid4().hex,
        "token_type": "token_type",
        "expires_in": access_token_expires_in,
        "refresh_token_expires_in": refresh_token_expires_in,
        "refresh_token": uuid.uuid4().hex,
    }


@pytest.fixture()
def storage_filename() -> str:
    return f"{TOKEN_FILE_PATH}/test_token.json"


@pytest.fixture()
def token_file_storage(storage_filename, token_data):
    data = token_data
    with open(storage_filename, "w") as f:
        json.dump(data, f)

    yield f.name

    pathlib.Path.unlink(pathlib.Path(f.name))
