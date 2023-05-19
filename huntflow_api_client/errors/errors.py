from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Error:
    type: str
    title: str
    location: Optional[dict] = None
    detail: Optional[str] = None


class ApiError(Exception):
    code: int = 500
    errors: List[Error]

    def __init__(self, code: Optional[int] = None, errors: Optional[List[Error]] = None):
        self.code = code or self.code
        self.errors = errors or []
        super().__init__()

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(code={self.code}, errors={self.errors})"


class BadRequestError(ApiError):
    code = 400


class AuthorizationError(ApiError):
    code = 401


class PaymentRequiredError(ApiError):
    code = 402


class AccessDeniedError(ApiError):
    code = 403


class NotFoundError(ApiError):
    code = 404


class TokenExpiredError(AuthorizationError):
    pass


class InvalidAccessTokenError(AuthorizationError):
    pass


class InvalidRefreshTokenError(ApiError):
    code = 404


class TooManyRequestsError(ApiError):
    code = 429
