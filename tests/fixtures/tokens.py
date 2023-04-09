import uuid
from pathlib import Path

import pytest

from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage
from tests.api import TokenPair, new_token_storage


@pytest.fixture
def token_pair() -> TokenPair:
    return TokenPair()


@pytest.fixture()
def token_filename(tmp_path: Path) -> Path:
    return tmp_path / (uuid.uuid4().hex + ".json")


@pytest.fixture
def token_storage(token_filename: str, token_pair: TokenPair) -> HuntflowTokenFileStorage:
    return new_token_storage(token_filename, token_pair)
