import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .locker import AbstractLocker
from .storage import AbstractHuntflowTokenStorage
from .token import ApiToken


class AbstractTokenProxy(ABC):
    @abstractmethod
    async def get_auth_header(self) -> Dict[str, str]:
        """Returns auth headers for requests"""
        pass

    @abstractmethod
    async def get_refresh_data(self) -> Dict[str, str]:
        """Returns data to use in refresh token request"""
        pass

    @abstractmethod
    async def update(self, refresh_result: Dict[str, Any]) -> None:
        """Save updated token to a persistent storage here if you need it"""
        pass

    async def lock_for_update(self) -> bool:
        """Non-blocking method to acquire lock before token refresh.
        Returns True if lock has been acquired successfully,
        False if the lock is already acquired.
        """
        return True

    async def release_lock(self) -> None:
        """Release previously acquired lock"""
        return

    async def is_updated(self) -> bool:
        """Returns True if the token has been changed since last `get_auth_header` call.
        Returns False otherwise.
        """
        return False


def convert_refresh_result_to_hf_token(
    refresh_result: Dict[str, Any],
    token: ApiToken,
) -> ApiToken:
    now = time.time()
    access_token = refresh_result["access_token"]
    refresh_token = refresh_result["refresh_token"] or token.refresh_token
    expiration_timestamp = now + refresh_result["expires_in"]
    last_refresh_timestamp = now
    return ApiToken(
        access_token=access_token,
        refresh_token=refresh_token,
        expiration_timestamp=expiration_timestamp,
        last_refresh_timestamp=last_refresh_timestamp,
    )


def get_auth_headers(token: ApiToken) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token.access_token}"}


def get_refresh_token_data(token: ApiToken) -> Dict[str, str]:
    assert token.refresh_token is not None
    return {"refresh_token": token.refresh_token}


class DummyHuntflowTokenProxy(AbstractTokenProxy):
    """Empty implementation of token proxy interface.
    Does nothing for token saving.
    It just implements necessary methods required for HF API client.
    Use it if you don't need to save refreshed tokens
    or don't need to refresh tokens at all.
    """

    def __init__(self, token: ApiToken):
        self._token = token

    async def get_auth_header(self) -> Dict[str, str]:
        return get_auth_headers(self._token)

    async def get_refresh_data(self) -> Dict[str, str]:
        return get_refresh_token_data(self._token)

    async def update(self, refresh_result: Dict[str, Any]) -> None:
        self._token = convert_refresh_result_to_hf_token(refresh_result, self._token)


class HuntflowTokenProxy(AbstractTokenProxy):
    """Ready to use TokenProxy implementation.
    It can read and update token via some implementation of
    AbstractHuntflowTokenStorage interface (e.g. HuntflowTokenFileStorage).
    Provide a lock object if you need to synchronize token updates across several
    coroutines (see `LocalLocker`), threads or processes.
    Also look at 'examples' directory for usage examples.
    """

    def __init__(
        self,
        storage: AbstractHuntflowTokenStorage,
        locker: Optional[AbstractLocker] = None,
    ):
        self._token: Optional[ApiToken] = None
        self._locker = locker
        self._storage = storage
        self._last_read_timestamp: Optional[float] = None

    async def get_auth_header(self) -> Dict[str, str]:
        await self._wait_for_free_lock()
        self._token = await self._storage.get()
        self._last_read_timestamp = time.time()
        return get_auth_headers(self._token)

    async def _wait_for_free_lock(self) -> bool:  # type: ignore[return]
        if self._locker is None:
            return True
        await self._locker.wait_for_lock()

    async def get_refresh_data(self) -> Dict[str, str]:
        self._token = await self._storage.get()
        return get_refresh_token_data(self._token)

    async def update(self, refresh_result: Dict[str, Any]) -> None:
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
        return await self._locker.acquire()

    async def release_lock(self) -> None:
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
