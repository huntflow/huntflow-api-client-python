import time
from datetime import datetime, timedelta
from typing import Dict, Any

from huntflow_api_client.tokens.proxy import HuntflowTokenProxy


async def test_get_auth_header__ok(
    huntflow_token_proxy: HuntflowTokenProxy,
    token_data: Dict[str, Any],
) -> None:
    access_token = token_data["access_token"]
    auth_header = await huntflow_token_proxy.get_auth_header()
    assert auth_header == {"Authorization": f"Bearer {access_token}"}


async def test_get_refresh_token_data__ok(
    huntflow_token_proxy: HuntflowTokenProxy,
    token_data: Dict[str, Any],
) -> None:
    refresh_token = token_data["refresh_token"]
    refresh_token_data = await huntflow_token_proxy.get_refresh_data()
    assert refresh_token_data == {"refresh_token": refresh_token}


async def test_update_token__ok(
    huntflow_token_proxy: HuntflowTokenProxy,
    token_data: Dict[str, Any],
    refresh_token_data: Dict[str, Any],
    freezer: Any,
) -> None:
    api_token = await huntflow_token_proxy._storage.get()
    assert api_token.dict() == token_data

    await huntflow_token_proxy.get_auth_header()

    tomorrow = datetime.now() + timedelta(days=1)
    freezer.move_to(tomorrow.isoformat())
    now = time.time()

    await huntflow_token_proxy.update(refresh_token_data)

    api_token = await huntflow_token_proxy._storage.get()
    assert api_token.dict() == {
        "access_token": refresh_token_data["access_token"],
        "refresh_token": refresh_token_data["refresh_token"],
        "expiration_timestamp": now + refresh_token_data["expires_in"],
        "last_refresh_timestamp": now,
    }

    assert await huntflow_token_proxy.is_updated()
