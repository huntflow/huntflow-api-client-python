import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict

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
    refresh_token_data: Dict[str, Any],
    token_storage_filename: str,
    freezer: Any,
) -> None:
    await huntflow_token_proxy.get_auth_header()

    tomorrow = datetime.now() + timedelta(days=1)
    freezer.move_to(tomorrow.isoformat())
    now = time.time()

    await huntflow_token_proxy.update(refresh_token_data)
    assert await huntflow_token_proxy.is_updated()

    updated_api_token = {}
    with open(token_storage_filename) as token_data_file:
        updated_api_token.update(json.load(token_data_file))

    assert updated_api_token == {
        "access_token": refresh_token_data["access_token"],
        "refresh_token": refresh_token_data["refresh_token"],
        "expiration_timestamp": now + refresh_token_data["expires_in"],
        "last_refresh_timestamp": now,
    }
