from huntflow_api_client.errors import TokenExpiredError


def autorefresh_tokens(api_request, refresh_method):
    async def run(*args, **kwargs):
        try:
            response = await api_request(*args, **kwargs)
            return response
        except TokenExpiredError:
            await refresh_method()
            response = await api_request(*args, **kwargs)
            return response
    return run
