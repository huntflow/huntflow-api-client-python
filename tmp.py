import asyncio

import httpx

from huntflow_api_client.errors.errors import (
    InvalidAccessTokenError,
    ApiError,
    InvalidRefreshTokenError,
)
from huntflow_api_client.errors.handlers import HANDLERS, AbstractErrorHandler
from huntflow_api_client.errors.utils import async_error_handler_deco

error_data = {
    "errors": [
        {
            "type": "authorization_error",
            "title": "error.robot_token.not_found",
            "detail": "token_expired",
        }
    ]
}
error = httpx.HTTPStatusError(
    "error",
    request=httpx.Request("GET", ""),
    response=httpx.Response(status_code=429, json=error_data),
)


@async_error_handler_deco
async def main():
    error = httpx.HTTPStatusError(
        "error",
        request=httpx.Request("GET", "https://domain/token/refresh"),
        response=httpx.Response(status_code=404, json=error_data),
    )
    raise error


asyncio.run(main())
