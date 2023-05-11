import json
import time
from datetime import datetime, timedelta
from typing import Any

from huntflow_api_client.tokens.locker import AsyncioLockLocker
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage
from tests.api import TokenPair, get_token_refresh_data


async def test_get_auth_header__ok(
    token_storage: HuntflowTokenFileStorage,
    token_pair: TokenPair,
) -> None:
    token_proxy = HuntflowTokenProxy(token_storage, AsyncioLockLocker())
    auth_header = await token_proxy.get_auth_header()
    assert auth_header == {"Authorization": f"Bearer {token_pair.access_token}"}


async def test_get_refresh_token_data__ok(
    token_storage: HuntflowTokenFileStorage,
    token_pair: TokenPair,
) -> None:
    token_proxy = HuntflowTokenProxy(token_storage, AsyncioLockLocker())
    refresh_token_data = await token_proxy.get_refresh_data()
    assert refresh_token_data == {"refresh_token": token_pair.refresh_token}


async def test_update_token__ok(
    token_storage: HuntflowTokenFileStorage,
    token_filename: str,
    freezer: Any,
) -> None:
    token_proxy = HuntflowTokenProxy(token_storage, AsyncioLockLocker())
    await token_proxy.get_auth_header()

    tomorrow = datetime.now() + timedelta(days=1)
    freezer.move_to(tomorrow.isoformat())
    now = time.time()

    new_token_pair = TokenPair()
    refresh_token_data = get_token_refresh_data(new_token_pair)

    await token_proxy.update(refresh_token_data)
    assert await token_proxy.is_updated()

    updated_api_token = {}
    with open(token_filename) as token_data_file:
        updated_api_token = json.load(token_data_file)

    assert updated_api_token == {
        "access_token": refresh_token_data["access_token"],
        "refresh_token": refresh_token_data["refresh_token"],
        "expiration_timestamp": now + refresh_token_data["expires_in"],
        "last_refresh_timestamp": now,
    }
