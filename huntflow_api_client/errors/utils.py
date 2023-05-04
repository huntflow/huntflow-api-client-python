from typing import Callable

import httpx

from huntflow_api_client.errors.handlers import HANDLERS


def async_error_handler_deco(func: Callable) -> Callable:
    async def inner(*args, **kwargs):  # type: ignore
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            error = e
            for handler in HANDLERS:
                if handler.handle_exception.code == e.response.status_code:
                    error = handler.process_exception(e)
        raise error

    return inner
