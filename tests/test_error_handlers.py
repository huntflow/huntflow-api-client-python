import json
from typing import Dict, List

import httpx
import pytest

from huntflow_api_client.errors import errors, handlers
from huntflow_api_client.errors.utils import async_error_handler_deco
from tests.utils import http_responses


def compose_error(response: httpx.Response) -> httpx.HTTPStatusError:
    request = httpx.Request("GET", "")
    return httpx.HTTPStatusError("", request=request, response=response)


def compose_source_errors(error_list: List[errors.Error]) -> Dict[str, List[Dict[str, str]]]:
    return {"errors": [item.dict(exclude_none=True) for item in error_list]}


def raise_error(error_to_raise: httpx.HTTPStatusError) -> None:
    raise error_to_raise


async def test_error_handler_deco() -> None:
    func = async_error_handler_deco(raise_error)
    error_to_raise = compose_error(response=http_responses.RESPONSE_NOT_FOUND)
    with pytest.raises(errors.NotFoundError):
        await func(error_to_raise)

    error_to_raise = compose_error(response=httpx.Response(1000))
    with pytest.raises(httpx.HTTPStatusError):
        await func(error_to_raise)


async def test_authorization_error_handler() -> None:
    http_error = compose_error(http_responses.RESPONSE_INVALID_TOKEN)
    custom_error = handlers.AuthorizationErrorHandler.process_exception(http_error)
    assert isinstance(custom_error, errors.InvalidAccessTokenError)
    assert json.loads(http_error.response.content) == compose_source_errors(custom_error.errors)

    http_error = compose_error(http_responses.RESPONSE_TOKEN_EXPIRED)
    custom_error = handlers.AuthorizationErrorHandler.process_exception(http_error)
    assert isinstance(custom_error, errors.TokenExpiredError)
    assert json.loads(http_error.response.content) == compose_source_errors(custom_error.errors)

    http_error = compose_error(httpx.Response(status_code=401, content=""))
    custom_error = handlers.AuthorizationErrorHandler.process_exception(http_error)
    assert isinstance(custom_error, errors.AuthorizationError)
    assert not custom_error.errors


async def test_bad_request_error_handler() -> None:
    http_error = compose_error(http_responses.RESPONSE_BAD_REQUEST)
    custom_error = handlers.BadRequestErrorHandler.process_exception(http_error)
    assert isinstance(custom_error, errors.BadRequestError)
    assert json.loads(http_error.response.content) == compose_source_errors(custom_error.errors)


async def test_not_found_error_handler() -> None:
    http_error = compose_error(http_responses.RESPONSE_NOT_FOUND)
    custom_error = handlers.NotFoundErrorHandler.process_exception(http_error)
    assert isinstance(custom_error, errors.NotFoundError)
    assert json.loads(http_error.response.content) == compose_source_errors(custom_error.errors)

    http_error = compose_error(http_responses.RESPONSE_INVALID_REFRESH)
    custom_error = handlers.NotFoundErrorHandler.process_exception(http_error)
    assert isinstance(custom_error, errors.InvalidRefreshTokenError)
    assert json.loads(http_error.response.content) == compose_source_errors(custom_error.errors)


async def test_too_many_requests_error_handler() -> None:
    http_error = compose_error(http_responses.RESPONSE_TOO_MANY_REQUESTS)
    custom_error = handlers.TooManyRequestsErrorHandler.process_exception(http_error)
    assert isinstance(custom_error, errors.TooManyRequestsError)
    assert json.loads(http_error.response.content) == compose_source_errors(custom_error.errors)
