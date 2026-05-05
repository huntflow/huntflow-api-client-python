[![](https://img.shields.io/pypi/pyversions/huntflow-api-client.svg)](https://pypi.org/project/huntflow-api-client/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# huntflow-api-client

Async Python client for the [Huntflow API](https://api.huntflow.ai/v2/docs). It wraps [httpx](https://www.python-httpx.org/), adds Bearer authentication, optional automatic token refresh, and typed helpers for major resources.

## Installation

```bash
pip install huntflow-api-client
```

Requires Python **3.8.1+**. Main dependencies: [httpx](https://www.python-httpx.org/), `pydantic` v2, `email-validator`.

## Integration overview

1. Obtain an access token (and optionally a refresh token) using the flows described in the [Huntflow API documentation](https://api.huntflow.ai/v2/docs) (OAuth, service account, or your Huntflow product settings — whichever applies to your integration).
2. Create a `HuntflowAPI` instance with your API base URL and either a static `ApiToken` (`token=`) or a `token_proxy=`. If both are supplied, **`token_proxy` wins** and `token` is ignored.
3. Call `await api.request(...)` for any endpoint, or use entity classes (e.g. `Applicant`, `Vacancy`) for typed request/response models.

The client appends `/v2` to `base_url` for all requests. Paths you pass to `request()` are relative to that versioned root (for example `GET` `"/accounts"`, not `"/v2/accounts"`).

### Base URL

The constructor default is `https://api.huntflow.dev` (development). For production, pass your real API host, for example:

```python
HuntflowAPI("https://api.huntflow.ai", token=token)
```

Use the base URL Huntflow provides for your environment (no trailing `/v2`).

## Quick start (access token only)

Minimal setup: pass `ApiToken` with an `access_token`. Fine for short scripts. For **persisted** refresh across restarts or processes, use **`HuntflowTokenProxy`** and storage (see [Token proxy, storage, and locks](#token-proxy-storage-and-locks)). You can still set **`auto_refresh_tokens=True`** with `token=` — refresh then updates the in-memory token only (see that section for details).

```python
import asyncio

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens.token import ApiToken


async def main() -> None:
    token = ApiToken(access_token="YOUR_ACCESS_TOKEN")
    api = HuntflowAPI("https://api.huntflow.ai", token=token)

    response = await api.request("GET", "/accounts")
    accounts = response.json()
    print(accounts)


asyncio.run(main())
```

## Using resource entities

Entity classes take a `HuntflowAPI` instance and return Pydantic models parsed from JSON.

```python
import asyncio

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import Applicant
from huntflow_api_client.tokens.token import ApiToken


async def main() -> None:
    api = HuntflowAPI(
        "https://api.huntflow.ai",
        token=ApiToken(access_token="YOUR_ACCESS_TOKEN"),
    )
    applicants = Applicant(api)

    page = await applicants.list(account_id=1, count=10, page=1)
    for item in page.items:
        print(item.id, item.first_name, item.last_name)


asyncio.run(main())
```

Other entities live under `huntflow_api_client.entities` (vacancies, webhooks, dictionaries, etc.). Each method docstring links to the matching OpenAPI operation where applicable.

## Token proxy, storage, and locks

`HuntflowAPI` authenticates every request using an **`AbstractTokenProxy`**. Most apps pass **`token=`** or **`token_proxy=HuntflowTokenProxy(...)`**. Subclass **`AbstractTokenProxy`** only for uncommon setups (custom token sources, extra logging, and so on).

- If you pass **`token=`** (`ApiToken`), the client wraps it in **`DummyHuntflowTokenProxy`**. With **`auto_refresh_tokens=True`**, refreshed tokens stay **in memory** on that proxy only (nothing is persisted). You still need **`refresh_token`** set on `ApiToken`, otherwise refresh cannot run.
- For persisted refresh, pass **`token_proxy=`** — typically **`HuntflowTokenProxy`**, which loads and saves tokens through **`AbstractHuntflowTokenStorage`**.

### Storage (`AbstractHuntflowTokenStorage`)

Implementations must:

- **`get()`** — return an `ApiToken` (at least `access_token`; include `refresh_token` if you use refresh).
- **`update(token)`** — persist the token after a successful `/token/refresh` (and any fields you care about, e.g. `expiration_timestamp`).

The built-in **`HuntflowTokenFileStorage`** reads/writes a JSON file with the same keys as `ApiToken` (`access_token`, `refresh_token`, optional timestamps). The file is overwritten on refresh.

### Locker (`AbstractLocker`)

When **`auto_refresh_tokens=True`**, several coroutines can hit token expiry at once. **`HuntflowTokenProxy`** can use a locker so only one refresh runs; others wait or retry.

- If **`locker=None`** (default), no synchronization is applied: concurrent refreshes are possible under load. Prefer a locker whenever **one storage** is shared by **many concurrent requests**.
- **`AsyncioLockLocker`** — sufficient for **one process / one event loop** (see [`examples/api_client_with_simple_locks.py`](examples/api_client_with_simple_locks.py)).
- For **multiple workers or hosts**, use a **distributed lock** (Redis, etc.) implementing **`AbstractLocker`**, together with storage that all instances share.

### Wiring `HuntflowTokenProxy`

```python
from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens.locker import AsyncioLockLocker
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage

storage = HuntflowTokenFileStorage("/secure/huntflow_token.json")
locker = AsyncioLockLocker()
token_proxy = HuntflowTokenProxy(storage, locker=locker)

api = HuntflowAPI(
    "https://api.huntflow.ai",
    token_proxy=token_proxy,
    auto_refresh_tokens=True,
)
```

Seed the JSON file once with `access_token` and `refresh_token` from Huntflow before starting.

### Example: Redis-backed storage and lock

The package does **not** depend on Redis; install it separately (`pip install "redis>=4.2"` so `redis.asyncio` and async locks behave consistently). Use one async Redis client for both storage and the lock. **Populate the token key** before the first API call (same JSON shape as the file storage).

```python
import asyncio
import json
import time
from typing import Any, Dict, Optional

from redis.asyncio import Redis
from redis.asyncio.lock import Lock
from redis.exceptions import LockError

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens.locker import AbstractLocker
from huntflow_api_client.tokens.proxy import (
    AbstractTokenProxy,
    convert_refresh_result_to_hf_token,
    get_auth_headers,
    get_refresh_token_data,
)
from huntflow_api_client.tokens.token import ApiToken

POLL_INTERVAL = 0.2


class RedisLockLocker(AbstractLocker):
    """Coordinates token refresh across concurrent workers.

    One caller acquires the lock and performs refresh; others wait until
    the lock is released and then continue with updated token data.
    """

    def __init__(self, redis: Redis, name: str = "huntflow:token_refresh") -> None:
        self._lock = Lock(redis, name=name, timeout=30.0, blocking=False)

    async def acquire(self) -> bool:
        try:
            return bool(await self._lock.acquire())
        except LockError:
            return False

    async def wait_for_lock(self) -> None:
        while await self._lock.locked():
            await asyncio.sleep(POLL_INTERVAL)

    async def release(self) -> None:
        try:
            await self._lock.release()
        except LockError:
            return


class RedisTokenAccessor:
    """Layer for token read/update operations.

    Keeps Redis calls in one place and exposes lock-related operations
    used by the proxy.
    """

    def __init__(
        self,
        redis: Redis,
        locker: AbstractLocker,
        token_key: str = "huntflow:token",
    ) -> None:
        self._redis = redis
        self._locker = locker
        self._token_key = token_key

    async def get(self, bypass_lock: bool = False) -> Optional[Dict[str, Any]]:
        if not bypass_lock:
            await self._locker.wait_for_lock()
        raw = await self._redis.get(self._token_key)
        if not raw:
            return None
        return json.loads(raw)

    async def update(self, token: ApiToken) -> None:
        await self._redis.set(self._token_key, json.dumps(token.dict()))

    async def lock_for_update(self) -> bool:
        return await self._locker.acquire()

    async def release_lock(self) -> None:
        await self._locker.release()


class RedisTokenProxy(AbstractTokenProxy):
    """`AbstractTokenProxy` implementation over accessor + locker.

    Returns auth headers, provides refresh payload, saves refreshed token,
    and checks whether another worker has already updated the token.
    """

    def __init__(self, accessor: RedisTokenAccessor) -> None:
        self._accessor = accessor
        self._token: Optional[ApiToken] = None
        self._last_read_timestamp: Optional[float] = None

    async def get_auth_header(self) -> Dict[str, str]:
        data = await self._accessor.get()
        if data is None:
            raise KeyError("Token not found in Redis. Seed access_token and refresh_token first.")
        self._token = ApiToken.from_dict(data)
        self._last_read_timestamp = time.time()
        return get_auth_headers(self._token)

    async def get_refresh_data(self) -> Dict[str, str]:
        if self._token is None:
            data = await self._accessor.get()
            if data is None:
                raise KeyError("Token not found in Redis. Seed access_token and refresh_token first.")
            self._token = ApiToken.from_dict(data)
        return get_refresh_token_data(self._token)

    async def update(self, refresh_result: dict) -> None:
        assert self._token is not None
        self._token = convert_refresh_result_to_hf_token(refresh_result, self._token)
        await self._accessor.update(self._token)

    async def lock_for_update(self) -> bool:
        return await self._accessor.lock_for_update()

    async def release_lock(self) -> None:
        await self._accessor.release_lock()

    async def is_updated(self) -> bool:
        if self._last_read_timestamp is None:
            return False
        current_data = await self._accessor.get(bypass_lock=True)
        if current_data is None:
            return False
        current = ApiToken.from_dict(current_data)
        last_refresh_timestamp = current.last_refresh_timestamp or 0.0
        return last_refresh_timestamp > self._last_read_timestamp


def build_api(redis: Redis) -> HuntflowAPI:
    locker = RedisLockLocker(redis, name="huntflow:token_refresh")
    accessor = RedisTokenAccessor(redis, locker=locker, token_key="huntflow:token")
    token_proxy = RedisTokenProxy(accessor)
    return HuntflowAPI(
        "https://api.huntflow.ai",
        token_proxy=token_proxy,
        auto_refresh_tokens=True,
    )
```

## Raw HTTP access

Every method on entities ultimately uses `HuntflowAPI.request`, which mirrors [`httpx.AsyncClient.request`](https://www.python-httpx.org/api/#asyncclient) (`json`, `params`, `files`, `timeout`, etc.). Entity methods usually serialize typed request models (for example `ApplicantCreateRequest.jsonable_dict(...)`); with `request()` you build the JSON yourself.

```python
account_id = 1
payload = {"first_name": "John", "last_name": "Doe"}  # match API schema

response = await api.request(
    "POST",
    f"/accounts/{account_id}/applicants",
    json=payload,
)
```

Errors from non-success status codes are turned into typed exceptions in `huntflow_api_client.errors` (for example `NotFoundError`, `BadRequestError`, `TokenExpiredError`, `AuthorizationError`).

## Links

- [Huntflow API v2 documentation](https://api.huntflow.ai/v2/docs)
- [Package on PyPI](https://pypi.org/project/huntflow-api-client/)
- [Source code](https://github.com/huntflow/huntflow-api-client-python)
