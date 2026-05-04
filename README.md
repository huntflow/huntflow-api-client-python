[![](https://img.shields.io/pypi/pyversions/huntflow-api-client.svg)](https://pypi.org/project/huntflow-api-client/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# huntflow-api-client

Async Python client for the [Huntflow API](https://api.huntflow.ai/v2/docs). It wraps [httpx](https://www.python-httpx.org/), adds Bearer authentication, optional automatic token refresh, and typed helpers for major resources.

**Async-only:** every `request()` and entity method is `async` — call them from `async def` code (`asyncio.run`, FastAPI routes, your own event loop, etc.). There is no synchronous client.

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
import json

from redis.asyncio import Redis
from redis.exceptions import LockError

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens.locker import AbstractLocker
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from huntflow_api_client.tokens.storage import AbstractHuntflowTokenStorage
from huntflow_api_client.tokens.token import ApiToken


class HuntflowTokenRedisStorage(AbstractHuntflowTokenStorage):
    def __init__(self, redis: Redis, key: str = "huntflow:token") -> None:
        self._redis = redis
        self._key = key

    async def get(self) -> ApiToken:
        raw = await self._redis.get(self._key)
        if raw is None:
            msg = (
                f"Redis key {self._key!r} is empty. "
                "SET JSON with access_token and refresh_token before use."
            )
            raise KeyError(msg)
        return ApiToken.from_dict(json.loads(raw))

    async def update(self, token: ApiToken) -> None:
        await self._redis.set(self._key, json.dumps(token.dict()))


class RedisLockLocker(AbstractLocker):
    """Distributed lock compatible with HuntflowTokenProxy (multi-worker)."""

    def __init__(self, redis: Redis, name: str = "huntflow:token_refresh") -> None:
        self._lock = redis.lock(name, timeout=30.0, blocking_timeout=60.0)

    async def acquire(self) -> bool:
        return bool(await self._lock.acquire(blocking=False))

    async def wait_for_lock(self) -> None:
        async with self._lock:
            pass

    async def release(self) -> None:
        try:
            await self._lock.release()
        except LockError:
            return


def build_api(redis: Redis) -> HuntflowAPI:
    storage = HuntflowTokenRedisStorage(redis, key="huntflow:token")
    locker = RedisLockLocker(redis, name="huntflow:token_refresh")
    token_proxy = HuntflowTokenProxy(storage, locker=locker)
    return HuntflowAPI(
        "https://api.huntflow.ai",
        token_proxy=token_proxy,
        auto_refresh_tokens=True,
    )


# redis = Redis.from_url("redis://localhost:6379/0", decode_responses=True)
# try:
#     api = build_api(redis)
#     ...
# finally:
#     await redis.aclose()
```

Tune lock **`timeout`** / **`blocking_timeout`** for your network and refresh latency. Keep the **`Redis`** instance for the app lifetime and **`await redis.aclose()`** on shutdown. For fully custom behavior (e.g. KMS-wrapped secrets), subclass **`AbstractTokenProxy`** instead of `HuntflowTokenProxy`.

## Raw HTTP access

Every method on entities ultimately uses `HuntflowAPI.request`, which mirrors [`httpx.AsyncClient.request`](https://www.python-httpx.org/api/#asyncclient) (`json`, `params`, `files`, `timeout`, etc.). Entity methods usually serialize typed request models (for example `ApplicantCreateRequest.jsonable_dict(...)`); with `request()` you build the JSON yourself.

```python
account_id = 1
payload = {"first_name": "Ada", "last_name": "Lovelace"}  # match API schema

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
