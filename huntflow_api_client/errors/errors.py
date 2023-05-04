import json
from typing import List, Optional
from pydantic import BaseModel


class Location(BaseModel):
    entity: str
    variable: str


class Error(BaseModel):
    type: str
    title: str
    location: Optional[Location] = None
    detail: Optional[str] = None


class ApiError(Exception):
    code: int = 500
    errors: List[Error]

    def __init__(self, *args, errors: Optional[List[Error]] = None):
        self.errors = errors or list()
        super().__init__(*args)

    def __str__(self):
        errors = [item.dict(exclude_none=True) for item in self.errors]
        return json.dumps({"Code": self.code, "Errors": errors}, indent=4, ensure_ascii=False)


class AuthorizationError(ApiError):
    code = 401


class BadRequestError(ApiError):
    code = 400


class NotFoundError(ApiError):
    code = 404


class TokenExpiredError(ApiError):
    code = 401


class InvalidAccessTokenError(ApiError):
    code = 401


class InvalidRefreshTokenError(ApiError):
    code = 404


class TooManyRequestsError(ApiError):
    code = 429
