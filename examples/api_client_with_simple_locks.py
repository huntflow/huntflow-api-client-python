import asyncio
import json
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from dataclasses import asdict
from datetime import datetime
from typing import Dict, Generic, TypeVar, List

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens import HuntflowApiTokens, AbstractTokenHandler


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
    raise TypeError("Type %s not serializable" % type(obj))


class FileBasedTokenStorage(AbstractTokenStorage[HuntflowApiTokens]):
    """Sample implementation of token storage interface.
    Token will be stored in a local file in json-serialized form.
    """
    def __init__(self, filename):
        self._filename = filename

    async def get(self) -> HuntflowApiTokens:
        # TODO: Need to use aiofiles
        with open(self._filename) as fin:
            data = json.load(fin)
        will_expires_at = data.get("will_expires_at")
        if will_expires_at:
            data["will_expires_at"] = datetime.fromisoformat(will_expires_at)
        return HuntflowApiTokens.from_dict(data)

    async def update(self, token: HuntflowApiTokens):
        # TODO: Need to use aiofiles
        with open(self._filename, "w") as fout:
            json.dump(asdict(token), fout, default=json_serial, indent=4)


class AlreadyLockedException(Exception):
    pass


class AsyncioLockTokenHandler(AbstractTokenHandler):
    """
    Sample implementation for token handler with locking
    and external token storage.
    It may be used for API client if you have one thread in your
    application with concurrent coroutines used api client.
    """
    auto_refresh: bool = True
    lock = asyncio.Lock()

    def __init__(
        self,
        *,
        api_tokens: HuntflowApiTokens,
        token_storage: AbstractTokenStorage,
        **kwargs,
    ) -> None:
        super().__init__(api_tokens=api_tokens, **kwargs)
        self.token_storage = token_storage

    async def get_auth_header(self) -> Dict[str, str]:
        await self._wait_for_free_lock()
        self._tokens = await self.token_storage.get()
        return await super().get_auth_header()

    @classmethod
    async def _wait_for_free_lock(cls):
        if not cls.lock.locked():
            return
        async with cls.lock:
            pass

    async def update_by_refresh_result(self, refresh_result: Dict) -> None:
        self._tokens = HuntflowApiTokens.from_api_response(refresh_result)
        await self.token_storage.update(self._tokens)

    @classmethod
    async def lock_for_update(cls):
        if cls.lock.locked():
            raise AlreadyLockedException()
        await cls.lock.acquire()

    @classmethod
    async def release_lock(cls):
        cls.lock.release()


async def get_and_print_org_info(api_client: HuntflowAPI):
    response = await api_client.request("GET", "/v2/accounts")
    print(response.json())


async def main(concurrent_client_count: int, token_filename: str, base_url: str):
    token_storage = FileBasedTokenStorage(token_filename)
    api_tokens = await token_storage.get()
    tokens_handler = AsyncioLockTokenHandler(
        api_tokens=api_tokens,
        token_storage=token_storage,
        refresh_token_lock=AsyncioLockTokenHandler.lock_for_update,
        release_refresh_lock=AsyncioLockTokenHandler.release_lock,
        already_locked_exception_cls=AlreadyLockedException,
    )
    api_clients: List[HuntflowAPI] = []
    for _ in range(concurrent_client_count):
        client = HuntflowAPI(base_url, tokens_handler=tokens_handler)
        api_clients.append(client)

    calls = [get_and_print_org_info(client) for client in api_clients]
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
