from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional


@dataclass
class HuntflowApiToken:
    access_token: str
    refresh_token: str
    will_expire_at: Optional[datetime]


def convert_refresh_result_to_hf_token(
    refresh_result: Dict,
    token: HuntflowApiToken,
) -> HuntflowApiToken:
    now = datetime.now()
    token.access_token = refresh_result["access_token"]
    token.refresh_token = refresh_result["refresh_token"] or token.refresh_token
    token.will_expire_at = now + timedelta(seconds=refresh_result["expires_in"])
    return token


def get_auth_headers(token: HuntflowApiToken) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token.access_token}"}


def get_refresh_token_data(token: HuntflowApiToken) -> Dict[str, str]:
        return {"refresh_token": token.refresh_token}


class AbstractTokenProxy(ABC):
    @abstractmethod
    async def get_auth_header(self) -> Dict[str, str]:
        """Return auth headers for requests"""
        pass

    @abstractmethod
    async def get_refresh_token_data(self) -> Dict[str, str]:
        """Returns data to use in refresh token request"""
        pass

    @abstractmethod
    async def update_by_refresh_result(self, refresh_result: Dict) -> None:
        """Save updated token to a persistent storage here if you need it"""
        pass


class HuntflowTokenProxyBase(AbstractTokenProxy):
    def __init__(self, token: HuntflowApiToken) -> None:
        self.token = token

    async def get_auth_header(self) -> Dict[str, str]:
        return get_auth_headers(self.token)

    async def get_refresh_token_data(self) -> Dict:
        return get_refresh_token_data(self.token)

    async def update_by_refresh_result(self, refresh_result: Dict) -> None:
        self.token = convert_refresh_result_to_hf_token(refresh_result, self.token)
