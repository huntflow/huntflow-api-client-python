import abc
from json import JSONDecodeError
from typing import Dict, List

import httpx

from huntflow_api_client.errors import (
    AccessDeniedError,
    ApiError,
    AuthorizationError,
    BadRequestError,
    Error,
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
    NotFoundError,
    PaymentRequiredError,
    TokenExpiredError,
    TooManyRequestsError,
)


class AbstractErrorHandler(abc.ABC):
    @staticmethod
    def _parse_errors(response: httpx.Response) -> List[Error]:
        errors = []
        try:
            body = response.json()
        except JSONDecodeError:
            pass
        else:
            for err in body.get("errors", []):
                errors.append(Error(**err))
        return errors

    @abc.abstractmethod
    def raise_exception(self, response: httpx.Response) -> None:
        pass


class DefaultErrorHandler(AbstractErrorHandler):
    def raise_exception(self, response: httpx.Response) -> None:
        """
        :param response: httpx.Response
        :raises ApiError
        """
        raise ApiError(code=response.status_code, errors=self._parse_errors(response))


class ErrorHandler400(AbstractErrorHandler):
    def raise_exception(self, response: httpx.Response) -> None:
        """
        :param response: httpx.Response
        :raises BadRequestError
        """
        raise BadRequestError(errors=self._parse_errors(response))


class ErrorHandler401(AbstractErrorHandler):
    def raise_exception(self, response: httpx.Response) -> None:
        """
        :param response: httpx.Response
        :raises AuthorizationError
        :raises InvalidAccessTokenError
        :raises TokenExpiredError
        """
        error_list = self._parse_errors(response)

        try:
            msg = error_list[0].detail
        except IndexError:
            msg = None

        if msg == "token_expired":
            raise TokenExpiredError(errors=error_list)
        elif msg == "Invalid access token":
            raise InvalidAccessTokenError(errors=error_list)

        raise AuthorizationError(errors=error_list)


class ErrorHandler402(AbstractErrorHandler):
    def raise_exception(self, response: httpx.Response) -> None:
        """
        :param response: httpx.Response
        :raises PaymentRequiredError
        """
        raise PaymentRequiredError(errors=self._parse_errors(response))


class ErrorHandler403(AbstractErrorHandler):
    def raise_exception(self, response: httpx.Response) -> None:
        """
        :param response: httpx.Response
        :raises AccessDeniedError
        """
        raise AccessDeniedError(errors=self._parse_errors(response))


class ErrorHandler404(AbstractErrorHandler):
    def raise_exception(self, response: httpx.Response) -> None:
        """
        :param response: httpx.Response
        :raises InvalidRefreshTokenError
        :raises NotFoundError
        """
        error_list = self._parse_errors(response)

        try:
            msg = error_list[0].title
        except IndexError:
            msg = None

        if msg == "error.robot_token.not_found":
            raise InvalidRefreshTokenError(errors=error_list)

        raise NotFoundError(errors=error_list)


class ErrorHandler429(AbstractErrorHandler):
    def raise_exception(self, response: httpx.Response) -> None:
        """
        :param response: httpx.Response
        :raises TooManyRequestsError
        """
        raise TooManyRequestsError(errors=self._parse_errors(response))


ERROR_HANDLERS: Dict[int, AbstractErrorHandler] = {
    400: ErrorHandler400(),
    401: ErrorHandler401(),
    402: ErrorHandler402(),
    403: ErrorHandler403(),
    404: ErrorHandler404(),
    429: ErrorHandler429(),
}
