import asyncio
from abc import ABC, abstractmethod


class AbstractLocker(ABC):
    @abstractmethod
    async def acquire(self) -> bool:
        """Non-blocking lock aqcuire.
        If there is the lock already, then return False.
        If the lock is not acquired, then acquire the lock and return True
        """
        return True

    @abstractmethod
    async def wait_for_lock(self) -> None:
        """Blocking lock check. If there is no locks, then return.
        If the lock is set, then wait for it's release.
        """
        pass

    @abstractmethod
    async def release(self) -> None:
        pass


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

    async def acquire(self) -> bool:
        """Non-blocking lock aqcuire.
        If there is the lock already, then return False.
        If the lock is not acquired, then acquire the lock and return True
        """
        if self._lock.locked():
            return False
        await self._lock.acquire()
        return True

    async def wait_for_lock(self) -> None:
        """Blocking lock check. If there is no locks, then return.
        If the lock is set, then wait for it's release.
        """
        async with self._lock:
            pass

    async def release(self) -> None:
        if not self._lock.locked():
            return
        self._lock.release()
