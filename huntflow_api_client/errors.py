class ApiError(Exception):
    pass


class TokenExpiredError(ApiError):
    pass


class InvalidAccessTokenError(ApiError):
    pass


class InvalidRefreshTokenError(ApiError):
    pass
