import asyncio
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from dataclasses import asdict
from datetime import datetime, timedelta
import json
from typing import Dict, Generic, Optional, TypeVar, List

from huntflow_api_client.token_proxy import (
    HuntflowApiToken,
    AbstractTokenProxy,
    convert_refresh_result_to_hf_token,
    get_auth_headers,
    get_refresh_token_data,
)
from huntflow_api_client import HuntflowAPI


_TokenDTO = TypeVar("_TokenDTO")


class AbstractTokenStorage(ABC, Generic[_TokenDTO]):
    @abstractmethod
    async def get(self) -> _TokenDTO:
        pass

    @abstractmethod
    async def update(self, token: _TokenDTO):
        pass


def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class FileBasedTokenStorage(AbstractTokenStorage[HuntflowApiToken]):
    """Sample implementation of token storage interface.
    Token will be stored in a local file in json-serialized form.
    """
    def __init__(self, filename):
        self._filename = filename

    async def get(self) -> HuntflowApiToken:
        with open(self._filename) as fin:
            data = json.load(fin)
        will_expire_at = data.get("will_expire_at")
        if will_expire_at:
            data["will_expire_at"] = datetime.fromisoformat(will_expire_at)
        else:
            data["will_expire_at"] = None
        return HuntflowApiToken(**data)

    async def update(self, token: HuntflowApiToken):
        with open(self._filename, "w") as fout:
            json.dump(asdict(token), fout, default=json_serial)


class AlreadyLockedException(Exception):
    pass


class HuntflowTokenProxyWithAsyncioLock(AbstractTokenProxy):
    """Sample implementation for token proxy with locking
    and external token storage.
    It may be used for API client if you have one thread in your
    application with concurrent coroutines used api client.
    """
    def __init__(self, token_storage: AbstractTokenStorage) -> None:
        self.token: Optional[HuntflowApiToken] = None
        self.token_storage = token_storage
        self.lock: Optional[asyncio.Lock] = None

    async def get_auth_header(self) -> Dict[str, str]:
        await self._wait_for_free_lock()
        self.token = await self.token_storage.get()
        return get_auth_headers(self.token)

    async def _wait_for_free_lock(self):
        if self.lock is None:
            return
        async with self.lock():
            pass

    async def get_refresh_token_data(self) -> Dict[str, str]:
        assert self.token is not None
        return get_refresh_token_data(self.token)

    async def update_by_refresh_result(self, refresh_result: Dict) -> None:
        assert self.token is not None
        self.token = convert_refresh_result_to_hf_token(refresh_result, self.token)
        await self.token_storage.update(self.token)

    async def lock_for_update(self, api_client):
        if self.lock is not None:
            raise AlreadyLockedException()
        self.lock = asyncio.Lock()
        await self.lock.acquire()

    async def release_lock(self):
        if self.lock is None:
            return
        self.lock.release()
        self.lock = None


async def get_and_print_org_info(api_client: HuntflowAPI):
    response = await api_client.request("GET", "/accounts")
    print(response.json())


async def main(concurrent_client_count: int, token_filename: str, base_url: str):
    token_storage = FileBasedTokenStorage(token_filename)
    token_proxy = HuntflowTokenProxyWithAsyncioLock(token_storage)
    api_clients: List[HuntflowAPI] = []
    for _ in range(concurrent_client_count):
        client = HuntflowAPI(
            base_url,
            None,
            token_proxy,
            auto_refresh_tokens=True,
            refresh_token_lock=token_proxy.lock_for_update,
            release_refresh_lock=token_proxy.release_lock,
            already_locked_exception_cls=AlreadyLockedException,
        )
        api_clients.append(client)
    calls = [
        get_and_print_org_info(client)
        for client in api_clients
    ]
    await asyncio.gather(*calls)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--url", type=str)
    parser.add_argument("--token-file", type=str)
    args = parser.parse_args()
    return args
    
if __name__ == "__main__":
    args = parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.count, args.token_file, args.url))
