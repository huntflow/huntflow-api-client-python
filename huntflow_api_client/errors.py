class ApiError(Exception):
    pass


class TokenExpiredError(ApiError):
    pass
