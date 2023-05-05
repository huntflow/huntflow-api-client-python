import json
from typing import Dict, List

import httpx
import pytest

from huntflow_api_client.errors import errors, handlers
from huntflow_api_client.errors.utils import convert_response_to_error
from tests.utils import http_responses


def compose_source_errors(error_list: List[errors.Error]) -> Dict[str, List[Dict[str, str]]]:
    return {"errors": [item.dict(exclude_none=True) for item in error_list]}


async def responser(response: httpx.Response) -> httpx.Response:
    return response


async def test_error_handler_deco() -> None:
    func = convert_response_to_error(responser)
    with pytest.raises(errors.NotFoundError):
        await func(http_responses.RESPONSE_NOT_FOUND)

    unexpected_response = httpx.Response(1000)
    assert unexpected_response == await func(unexpected_response)


async def test_authorization_error_handler() -> None:
    custom_error = handlers.AuthorizationErrorHandler.process_response(
        http_responses.RESPONSE_INVALID_TOKEN,
    )
    assert isinstance(custom_error, errors.InvalidAccessTokenError)
    assert json.loads(http_responses.RESPONSE_INVALID_TOKEN.content) == compose_source_errors(
        custom_error.errors,
    )

    custom_error = handlers.AuthorizationErrorHandler.process_response(
        http_responses.RESPONSE_TOKEN_EXPIRED,
    )
    assert isinstance(custom_error, errors.TokenExpiredError)
    assert json.loads(http_responses.RESPONSE_TOKEN_EXPIRED.content) == compose_source_errors(
        custom_error.errors,
    )

    response = httpx.Response(status_code=401, content="")
    custom_error = handlers.AuthorizationErrorHandler.process_response(response)
    assert isinstance(custom_error, errors.AuthorizationError)
    assert not custom_error.errors


async def test_bad_request_error_handler() -> None:
    custom_error = handlers.BadRequestErrorHandler.process_response(
        http_responses.RESPONSE_BAD_REQUEST,
    )
    assert isinstance(custom_error, errors.BadRequestError)
    assert json.loads(http_responses.RESPONSE_BAD_REQUEST.content) == compose_source_errors(
        custom_error.errors,
    )


async def test_not_found_error_handler() -> None:
    custom_error = handlers.NotFoundErrorHandler.process_response(http_responses.RESPONSE_NOT_FOUND)
    assert isinstance(custom_error, errors.NotFoundError)
    assert json.loads(http_responses.RESPONSE_NOT_FOUND.content) == compose_source_errors(
        custom_error.errors,
    )

    custom_error = handlers.NotFoundErrorHandler.process_response(
        http_responses.RESPONSE_INVALID_REFRESH,
    )
    assert isinstance(custom_error, errors.InvalidRefreshTokenError)
    assert json.loads(http_responses.RESPONSE_INVALID_REFRESH.content) == compose_source_errors(
        custom_error.errors,
    )


async def test_too_many_requests_error_handler() -> None:
    custom_error = handlers.TooManyRequestsErrorHandler.process_response(
        http_responses.RESPONSE_TOO_MANY_REQUESTS,
    )
    assert isinstance(custom_error, errors.TooManyRequestsError)
    assert json.loads(http_responses.RESPONSE_TOO_MANY_REQUESTS.content) == compose_source_errors(
        custom_error.errors,
    )
