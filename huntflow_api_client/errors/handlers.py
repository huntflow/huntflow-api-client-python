import json
from typing import Generic, TypeVar, Type, List, Union, Dict
import httpx

from huntflow_api_client.errors import errors

EntityType = TypeVar("EntityType", bound=errors.ApiError)


class AbstractErrorHandler(Generic[EntityType]):
    handle_exception: Type[EntityType] = errors.ApiError

    @staticmethod
    def _get_response_errors(e: httpx.HTTPStatusError) -> List[Dict[str, str]]:
        content = e.response.content
        if not content:
            return []
        content = json.loads(content)
        return content.get("errors", [])

    @classmethod
    def process_exception(cls, e: httpx.HTTPStatusError) -> EntityType:
        error_list = cls._get_response_errors(e)
        result: List[errors.Error] = []

        for error in error_list:
            error = errors.Error.parse_obj(error)
            result.append(error)

        return cls.handle_exception(errors=result)


class AuthorizationErrorHandler(AbstractErrorHandler[errors.AuthorizationError]):
    handle_exception = errors.AuthorizationError

    @classmethod
    def process_exception(
        cls,
        e: httpx.HTTPStatusError,
    ) -> Union[errors.AuthorizationError, errors.InvalidAccessTokenError, errors.TokenExpiredError]:
        error_list = cls._get_response_errors(e)
        result: List[errors.Error] = []

        for error in error_list:
            error = errors.Error.parse_obj(error)
            result.append(error)

        try:
            msg = error_list[0]["detail"]
        except (KeyError, IndexError):
            msg = None

        if msg == "token_expired":
            return errors.TokenExpiredError(errors=result)
        if msg == "Invalid access token":
            return errors.InvalidAccessTokenError(errors=result)

        return errors.AuthorizationError(errors=result)


class BadRequestErrorHandler(AbstractErrorHandler[errors.BadRequestError]):
    handle_exception = errors.BadRequestError


class NotFoundErrorHandler(AbstractErrorHandler[errors.NotFoundError]):
    handle_exception = errors.NotFoundError

    @classmethod
    def process_exception(
        cls,
        e: httpx.HTTPStatusError,
    ) -> Union[errors.NotFoundError, errors.InvalidRefreshTokenError]:
        error_list = cls._get_response_errors(e)
        result: List[errors.Error] = []
        for error in error_list:
            error = errors.Error.parse_obj(error)
            result.append(error)

        try:
            msg = error_list[0]["title"]
        except (KeyError, IndexError):
            msg = None

        if msg == "error.robot_token.not_found":
            return errors.InvalidRefreshTokenError(errors=result)
        return errors.NotFoundError(errors=result)


class TooManyRequestsErrorHandler(AbstractErrorHandler[errors.TooManyRequestsError]):
    handle_exception = errors.TooManyRequestsError


HANDLERS = (
    AuthorizationErrorHandler,
    BadRequestErrorHandler,
    NotFoundErrorHandler,
    TooManyRequestsErrorHandler,
)
