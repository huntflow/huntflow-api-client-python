from typing import Callable

from huntflow_api_client.errors.handlers import HANDLERS


def convert_response_to_error(func: Callable) -> Callable:
    async def inner(*args, **kwargs):  # type: ignore
        response = await func(*args, **kwargs)
        for handler in HANDLERS:
            if handler.handle_exception.code == response.status_code:
                raise handler.process_response(response)
        return response

    return inner
