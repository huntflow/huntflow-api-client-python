from typing import Callable
from huntflow_api_client.errors.handlers import HANDLERS
import httpx


def async_error_handler_deco(func: Callable) -> Callable:
    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            for handler in HANDLERS:
                if handler.handle_exception.code == e.response.status_code:
                    raise handler.process_exception(e)
            raise

    return inner
