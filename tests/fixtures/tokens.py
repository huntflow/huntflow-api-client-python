import json
import uuid
from typing import Any, Dict, Optional

import pytest

from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage

ACCESS_TOKEN_EXPIRES_IN = 86400 * 7
REFRESH_TOKEN_EXPIRES_IN = 86400 * 14


class TokenPair:
    def __init__(self, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        self.access_token = access_token or uuid.uuid4().hex
        self.refresh_token = refresh_token or uuid.uuid4().hex


@pytest.fixture
def token_pair():
    return TokenPair()


@pytest.fixture()
def token_filename(tmp_path) -> str:
    return tmp_path / (uuid.uuid4().hex + ".json")


def new_token_storage(file_name: str, token_pair: TokenPair) -> HuntflowTokenFileStorage:
    token_data = {
        "access_token": token_pair.access_token,
        "refresh_token": token_pair.refresh_token,
    }
    with open(file_name, "w") as fout:
        json.dump(token_data, fout)
    storage = HuntflowTokenFileStorage(file_name)
    return storage


@pytest.fixture
def token_storage(token_filename: str, token_pair: TokenPair) -> HuntflowTokenFileStorage:
    return new_token_storage(token_filename, token_pair)


def get_token_refresh_data(token_pair: TokenPair) -> Dict[str, Any]:
    return {
        "access_token": token_pair.access_token,
        "expires_in": ACCESS_TOKEN_EXPIRES_IN,
        "refresh_token_expires_in": REFRESH_TOKEN_EXPIRES_IN,
        "refresh_token": token_pair.refresh_token,
    }
