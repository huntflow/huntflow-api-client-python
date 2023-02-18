from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from datetime import datetime, timedelta
from typing import Dict, Callable, Optional, Type


@dataclass
class HuntflowApiTokens:
    access_token: str
    refresh_token: Optional[str] = None
    will_expires_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, dict_: dict):
        attrs = {field.name for field in fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in attrs})

    @classmethod
    def from_api_response(cls, dict_: dict):
        attrs = {field.name for field in fields(cls)}
        dict_["will_expires_at"] = datetime.now() + timedelta(seconds=dict_["expires_in"])
        return cls(**{k: v for k, v in dict_.items() if k in attrs})


class AbstractTokenHandler(ABC):
    auto_refresh: bool = False

    def __init__(
        self,
        *,
        api_tokens: HuntflowApiTokens,
        refresh_token_lock: Optional[Callable] = None,
        release_refresh_lock: Optional[Callable] = None,
        already_locked_exception_cls: Optional[Type[Exception]] = None,
        **kwargs,
    ):
        if self.auto_refresh and not api_tokens.refresh_token:
            raise ValueError("Refresh token is required")

        invalid_arguments_for_refreshing = (
            refresh_token_lock is not None
            and not all((release_refresh_lock, already_locked_exception_cls))
        )
        if invalid_arguments_for_refreshing:
            raise Exception(
                "If refresh_token_lock is specified, then you have to provide "
                "release_refresh_lock and already_locked_exception_cls also"
            )

        self._tokens = api_tokens
        self._refresh_token_lock = refresh_token_lock
        self._release_refresh_lock = release_refresh_lock
        self._already_locked_exception_cls = already_locked_exception_cls

    async def get_auth_header(self) -> Dict[str, str]:
        """Returns Authorization header for request"""
        return {"Authorization": f"Bearer {self._tokens.access_token}"}

    async def get_refresh_token_data(self) -> Dict[str, str]:
        """Returns data to use in refresh token request"""
        return {"refresh_token": self._tokens.refresh_token}

    @abstractmethod
    async def update_by_refresh_result(self, refresh_result: Dict) -> None:
        """Save updated tokens to a persistent storage here if you need it"""
        pass

    async def set_lock_for_update(self) -> bool:
        """Attempts to set a lock on refreshing tokens"""
        if self._refresh_token_lock is None:
            return True
        try:
            await self._refresh_token_lock()
        except self._already_locked_exception_cls:
            return False
        return True

    async def release_lock_for_update(self):
        """Releases lock"""
        if self._release_refresh_lock is None:
            return
        await self._release_refresh_lock()


class DummyTokenHandler(AbstractTokenHandler):
    """Stub that does nothing useful"""

    def __init__(self, api_tokens: HuntflowApiTokens, **kwargs) -> None:
        super().__init__(api_tokens=api_tokens, **kwargs)

    async def update_by_refresh_result(self, refresh_result: Dict) -> None:
        pass
