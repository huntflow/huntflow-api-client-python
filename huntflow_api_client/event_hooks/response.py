import httpx

from huntflow_api_client.errors import TokenExpiredError, InvalidAccessTokenError


async def raise_token_expired_hook(response: httpx.Response):
    if response.status_code == 401:
        if not hasattr(response, "_content"):
            await response.aread()
        data = response.json()
        try:
            msg = data["errors"][0]["detail"]
        except KeyError:
            msg = None

        if msg == "token_expired":
            raise TokenExpiredError()
        if msg == "Invalid access token":
            raise InvalidAccessTokenError()
