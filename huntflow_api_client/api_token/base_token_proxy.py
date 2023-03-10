from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional


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
    async def update(self, refresh_result: Dict) -> None:
        """Save updated token to a persistent storage here if you need it"""
        pass

    async def lock_for_update(self) -> bool:
        """Non-blocking method to acquire lock before token refresh.
        Returns True if lock has been acquired successfully,
        False if the lock is already acquired.
        """
        return True

    async def release_lock(self):
        """Release previously acquired lock"""
        pass

    async def is_updated(self) -> bool:
        """Returns True if the token has been changed since last `get_auth_header` call.
        Returns False otherwise.
        """
        return False


class AbstractLocker(ABC):
    @abstractmethod
    async def try_lock(self) -> bool:
        """Non-blocking lock aqcuire.
        If there is the lock already, then return False.
        If the lock is not acquired, then acquire the lock and return True
        """
        return True

    @abstractmethod
    async def wait_for_lock(self):
        """Blocking lock check. If there is no locks, then return.
        If the lock is set, then wait for it's release.
        """
        pass

    @abstractmethod
    async def release(self):
        pass
