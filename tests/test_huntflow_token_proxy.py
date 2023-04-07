import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .helpers import get_huntflow_token_proxy, get_refresh_token_data, get_token_data


async def test_get_auth_header__ok(tmp_path: Path) -> None:
    proxy, storage = get_huntflow_token_proxy(tmp_path)

    token_data = get_token_data(storage)
    auth_header = await proxy.get_auth_header()

    assert auth_header == {"Authorization": f"Bearer {token_data['access_token']}"}


async def test_get_refresh_token_data__ok(tmp_path: Path) -> None:
    proxy, storage = get_huntflow_token_proxy(tmp_path)

    token_data = get_token_data(storage)
    refresh_token_data = await proxy.get_refresh_data()

    assert refresh_token_data == {"refresh_token": token_data["refresh_token"]}


async def test_update_token__ok(tmp_path: Path, freezer: Any) -> None:
    proxy, storage = get_huntflow_token_proxy(tmp_path)
    await proxy.get_auth_header()

    tomorrow = datetime.now() + timedelta(days=1)
    freezer.move_to(tomorrow.isoformat())
    now = time.time()

    refresh_token_data = get_refresh_token_data()

    await proxy.update(refresh_token_data)
    assert await proxy.is_updated()

    updated_token_data = get_token_data(storage)
    assert updated_token_data == {
        "access_token": refresh_token_data["access_token"],
        "refresh_token": refresh_token_data["refresh_token"],
        "expiration_timestamp": now + refresh_token_data["expires_in"],
        "last_refresh_timestamp": now,
    }
