import json
from typing import Any, Dict, Generic, List, Tuple, Type, TypeVar, Union

import httpx

from huntflow_api_client.errors import errors

BaseApiErrorEntity = TypeVar("BaseApiErrorEntity", bound=errors.BaseApiError)


class BaseErrorHandler(Generic[BaseApiErrorEntity]):
    """
    A base class that converts HTTPStatusErrors to custom API errors.
    """

    handle_exception: Type[BaseApiErrorEntity]

    @staticmethod
    def _get_response_errors(response: httpx.Response) -> List[errors.Error]:
        content: bytes = response.content
        if not content:
            return []

        content_data: Dict[str, Any] = json.loads(content)
        error_list = content_data.get("errors", [])
        result: List[errors.Error] = []

        for error in error_list:
            error = errors.Error.parse_obj(error)
            result.append(error)
        return result

    @classmethod
    def process_response(cls, response: httpx.Response) -> BaseApiErrorEntity:
        error_list = cls._get_response_errors(response)
        return cls.handle_exception(errors=error_list)


class AuthorizationErrorHandler(
    BaseErrorHandler[
        Union[
            errors.AuthorizationError,
            errors.InvalidAccessTokenError,
            errors.TokenExpiredError,
        ],
    ],
):
    handle_exception = errors.AuthorizationError

    @classmethod
    def process_response(
        cls,
        response: httpx.Response,
    ) -> Union[errors.AuthorizationError, errors.InvalidAccessTokenError, errors.TokenExpiredError]:
        error_list = cls._get_response_errors(response)

        try:
            msg = error_list[0].detail
        except IndexError:
            msg = None

        if msg == "token_expired":
            return errors.TokenExpiredError(errors=error_list)
        if msg == "Invalid access token":
            return errors.InvalidAccessTokenError(errors=error_list)

        return errors.AuthorizationError(errors=error_list)


class BadRequestErrorHandler(BaseErrorHandler[errors.BadRequestError]):
    handle_exception = errors.BadRequestError


class NotFoundErrorHandler(
    BaseErrorHandler[
        Union[
            errors.NotFoundError,
            errors.InvalidRefreshTokenError,
        ],
    ],
):
    handle_exception = errors.NotFoundError

    @classmethod
    def process_response(
        cls,
        response: httpx.Response,
    ) -> Union[errors.NotFoundError, errors.InvalidRefreshTokenError]:
        error_list = cls._get_response_errors(response)

        try:
            msg = error_list[0].title
        except IndexError:
            msg = None

        if msg == "error.robot_token.not_found":
            return errors.InvalidRefreshTokenError(errors=error_list)
        return errors.NotFoundError(errors=error_list)


class TooManyRequestsErrorHandler(BaseErrorHandler[errors.TooManyRequestsError]):
    handle_exception = errors.TooManyRequestsError


class PaymentRequiredErrorHandler(BaseErrorHandler[errors.PaymentRequiredError]):
    handle_exception = errors.PaymentRequiredError


class AccessDeniedErrorHandler(BaseErrorHandler[errors.AccessDeniedError]):
    handle_exception = errors.AccessDeniedError


class InternalApiErrorHandler(BaseErrorHandler[errors.InternalApiError]):
    handle_exception = errors.InternalApiError


HANDLERS: Tuple = (
    AuthorizationErrorHandler,
    BadRequestErrorHandler,
    NotFoundErrorHandler,
    TooManyRequestsErrorHandler,
    PaymentRequiredErrorHandler,
    AccessDeniedErrorHandler,
    InternalApiErrorHandler,
)
