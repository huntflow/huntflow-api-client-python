import time
from datetime import datetime, timedelta


async def test_get_auth_header__ok(huntflow_token_proxy, token_data):
    access_token = token_data["access_token"]
    auth_header = await huntflow_token_proxy.get_auth_header()
    assert auth_header == {"Authorization": f"Bearer {access_token}"}


async def test_get_refresh_token_data__ok(huntflow_token_proxy, token_data):
    refresh_token = token_data["refresh_token"]
    refresh_token_data = await huntflow_token_proxy.get_refresh_data()
    assert refresh_token_data == {"refresh_token": refresh_token}


async def test_update_token__ok(huntflow_token_proxy, token_data, refresh_token_data, freezer):
    api_token = await huntflow_token_proxy._storage.get()
    assert api_token.dict() == token_data

    await huntflow_token_proxy.get_auth_header()

    next_day = datetime.now() + timedelta(days=10)
    freezer.move_to(next_day.isoformat())
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
