import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Tuple

from huntflow_api_client.tokens.locker import AsyncioLockLocker
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage

TEST_TOKEN_FILE_NAME: str = "test_token.json"
ACCESS_TOKEN_EXPIRES_IN: int = 86400 * 7  # expiration time in seconds
REFRESH_TOKEN_EXPIRES_IN: int = 86400 * 14  # expiration time in seconds


def get_huntflow_token_proxy(path: Path) -> Tuple[HuntflowTokenProxy, str]:
    now = time.time()
    data = {
        "access_token": uuid.uuid4().hex,
        "refresh_token": uuid.uuid4().hex,
        "expiration_timestamp": now + ACCESS_TOKEN_EXPIRES_IN,
        "last_refresh_timestamp": now,
    }
    with open(f"{path}/{TEST_TOKEN_FILE_NAME}", "w") as f:
        json.dump(data, f)

    return (
        HuntflowTokenProxy(locker=AsyncioLockLocker(), storage=HuntflowTokenFileStorage(f.name)),
        f.name,
    )


def get_refresh_token_data() -> Dict[str, Any]:
    return {
        "access_token": uuid.uuid4().hex,
        "token_type": "token_type",
        "expires_in": ACCESS_TOKEN_EXPIRES_IN,
        "refresh_token_expires_in": REFRESH_TOKEN_EXPIRES_IN,
        "refresh_token": uuid.uuid4().hex,
    }


def get_token_data(filename: str) -> Dict[str, Any]:
    token_data = {}
    with open(filename) as f:
        token_data.update(json.load(f))

    return token_data
