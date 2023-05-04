import json
from typing import List, Optional

from pydantic import BaseModel


class Location(BaseModel):
    entity: str
    variable: str  # noqa VNE002


class Error(BaseModel):
    type: str  # noqa A003 VNE003
    title: str
    location: Optional[Location] = None
    detail: Optional[str] = None


class ApiError(Exception):
    code: int = 500
    errors: List[Error]

    def __init__(self, *args, errors: Optional[List[Error]] = None):  # type: ignore
        self.errors = errors or []
        super().__init__(*args)

    def __str__(self):  # type: ignore
        errors = [item.dict(exclude_none=True) for item in self.errors]
        return json.dumps({"Code": self.code, "Errors": errors}, indent=4, ensure_ascii=False)


class AuthorizationError(ApiError):
    code = 401


class BadRequestError(ApiError):
    code = 400


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
