import httpx

from huntflow_api_client.errors.handlers import ERROR_HANDLERS, DefaultErrorHandler


async def raise_for_status(response: httpx.Response) -> None:
    if response.status_code >= 400:
        await response.aread()
        err_handler = ERROR_HANDLERS.get(response.status_code, DefaultErrorHandler())
        err_handler.raise_exception(response)
