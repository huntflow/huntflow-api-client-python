import asyncio
import time
from typing import Dict, Optional

from .base_token_proxy import AbstractTokenProxy, AbstractLocker
from .huntflow_token import HuntflowApiToken
from .huntflow_token_storage import AbstractHuntflowTokenStorage


def convert_refresh_result_to_hf_token(
    refresh_result: Dict,
    token: HuntflowApiToken,
) -> HuntflowApiToken:
    now = time.time()
    access_token = refresh_result["access_token"]
    refresh_token = refresh_result["refresh_token"] or token.refresh_token
    expiration_timestamp = now + refresh_result["expires_in"]
    last_refresh_timestamp = now
    return HuntflowApiToken(
        access_token=access_token,
        refresh_token=refresh_token,
        expiration_timestamp=expiration_timestamp,
        last_refresh_timestamp=last_refresh_timestamp,
    )


def get_auth_headers(token: HuntflowApiToken) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token.access_token}"}


def get_refresh_token_data(token: HuntflowApiToken) -> Dict[str, str]:
    assert token.refresh_token is not None
    return {"refresh_token": token.refresh_token}


class DummyHuntflowTokenProxy(AbstractTokenProxy):
    """Empty implementation of token proxy interface.
    Does nothing for token saving.
    It just implements necessary methods required for HF API client.
    Use it if you don't need to save refreshed tokens
    or don't need to refresh tokens at all.
    """
    def __init__(self, token: HuntflowApiToken):
        self._token = token
    
    async def get_auth_header(self) -> Dict[str, str]:
        return get_auth_headers(self._token)

    async def get_refresh_data(self) -> Dict:
        return get_refresh_token_data(self._token)

    async def update(self, refresh_result: Dict) -> None:
        self._token = convert_refresh_result_to_hf_token(refresh_result, self._token)


class AsyncioLockLocker(AbstractLocker):
    """Simple implementation of locker interface.
    It may be used if you need to synchronize token refresh across several
    coroutines in a single thread.
    Warning: Do not use it if you need to synchronize token updates via several threads
    of processes.
    In case of several processes you have to implement some distributed locking mechanism.
    Which one to use depends of your infrastructure (redis, etcd, whatever).
    """
    def __init__(self) -> None:
        self._lock: asyncio.Lock = asyncio.Lock()

    async def try_lock(self) -> bool:
        """Non-blocking lock aqcuire.
        If there is the lock already, then return False.
        If the lock is not acquired, then acquire the lock and return True
        """
        if self._lock.locked():
            return False
        await self._lock.acquire()
        return True

    async def wait_for_lock(self):
        """Blocking lock check. If there is no locks, then return.
        If the lock is set, then wait for it's release.
        """
        async with self._lock:
            pass

    async def release(self):
        if not self._lock.locked():
            return
        self._lock.release()


class HuntflowTokenProxy(AbstractTokenProxy):
    """Ready to use TokenProxy implementation.
    It can read and update token via some implementation of
    AbstractHuntflowTokenStorage interface (e.g. HuntflowTokenFileStorage).
    Provide a lock object if you need to synchronize token updates across several
    coroutines (see `LocalLocker`), threads or processes.
    Also look at 'examples' directory for usage examples.
    """
    def __init__(self, storage: AbstractHuntflowTokenStorage, locker: Optional[AbstractLocker] = None):
        self._token: Optional[HuntflowApiToken] = None
        self._locker = locker
        self._storage = storage
        self._last_read_timestamp: Optional[float] = None

    async def get_auth_header(self) -> Dict[str, str]:
        await self._wait_for_free_lock()
        self._token = await self._storage.get()
        self._last_read_timestamp = time.time()
        return get_auth_headers(self._token)

    async def _wait_for_free_lock(self):
        if self._locker is None:
            return True
        await self._locker.wait_for_lock()

    async def get_refresh_data(self) -> Optional[Dict]:
        self._token = await self._storage.get()
        return get_refresh_token_data(self._token)

    async def update(self, refresh_result: Dict) -> None:
        assert self._token
        self._token = convert_refresh_result_to_hf_token(refresh_result, self._token)
        await self._storage.update(self._token)

    async def lock_for_update(self) -> bool:
        """Non-blocking method to acquire lock before token refresh.
        Returns True if lock has been acquired successfully,
        False if the lock is already acquired.
        """
        if self._locker is None:
            return True
        return await self._locker.try_lock()

    async def release_lock(self):
        """Release previously acquired lock"""
        if self._locker is None:
            return
        await self._locker.release()

    async def is_updated(self) -> bool:
        if self._last_read_timestamp is None:
            return False
        token = await self._storage.get()
        last_refresh_timestamp = token.last_refresh_timestamp or 0.0
        return last_refresh_timestamp > self._last_read_timestamp
