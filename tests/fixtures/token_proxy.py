import pytest

from huntflow_api_client.tokens.locker import AsyncioLockLocker
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage


@pytest.fixture()
def huntflow_token_file_storage(token_file_storage: str) -> HuntflowTokenFileStorage:
    return HuntflowTokenFileStorage(token_file_storage)


@pytest.fixture()
def asyncio_lock_locker() -> AsyncioLockLocker:
    return AsyncioLockLocker()


@pytest.fixture()
def huntflow_token_proxy(
    asyncio_lock_locker: AsyncioLockLocker,
    huntflow_token_file_storage: HuntflowTokenFileStorage,
) -> HuntflowTokenProxy:
    return HuntflowTokenProxy(
        locker=asyncio_lock_locker,
        storage=huntflow_token_file_storage,
    )
