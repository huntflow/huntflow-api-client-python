import pytest

from tests.api import FakeAPIServer, TokenPair


@pytest.fixture()
def fake_server(token_pair: TokenPair) -> FakeAPIServer:
    return FakeAPIServer(token_pair)
