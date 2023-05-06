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


class InvalidRefreshTokenError(NotFoundError):
    pass


class TooManyRequestsError(ApiError):
    code = 429
