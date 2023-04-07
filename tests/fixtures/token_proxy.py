import pytest

from huntflow_api_client.tokens.locker import AsyncioLockLocker
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage


@pytest.fixture
def huntflow_token_proxy(token_storage: HuntflowTokenFileStorage) -> HuntflowTokenProxy:
    locker = AsyncioLockLocker()
    return HuntflowTokenProxy(locker=locker, storage=token_storage)
