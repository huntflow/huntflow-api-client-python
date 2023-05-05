import httpx

RESPONSE_TOKEN_EXPIRED = httpx.Response(
    status_code=401,
    json={
        "errors": [
            {
                "type": "authorization_error",
                "title": "Authorization Error",
                "detail": "token_expired",
            },
        ],
    },
)

RESPONSE_INVALID_TOKEN = httpx.Response(
    status_code=401,
    json={
        "errors": [
            {
                "type": "authorization_error",
                "title": "Authorization Error",
                "detail": "Invalid access token",
            },
        ],
    },
)

RESPONSE_BAD_REQUEST = httpx.Response(
    status_code=400,
    json={
        "errors": [
            {
                "type": "value_error.missing",
                "title": "field required",
                "location": {
                    "entity": "body",
                    "variable": "/account_division",
                },
            },
        ],
    },
)


RESPONSE_NOT_FOUND = httpx.Response(
    404,
    json={
        "errors": [
            {
                "type": "not_found",
                "title": "Unknown vacancy request",
            },
        ],
    },
)

RESPONSE_INVALID_REFRESH = httpx.Response(
    404,
    json={
        "errors": [
            {
                "type": "not_found",
                "title": "error.robot_token.not_found",
            },
        ],
    },
)

RESPONSE_TOO_MANY_REQUESTS = httpx.Response(
    429,
    json={
        "errors": [
            {
                "type": "too_many_requests",
                "title": "Answer request created too frequently",
            },
        ],
    },
)


RESPONSE_PAYMENT_REQUIRED = httpx.Response(
    402,
    json={
        "errors": [
            {
                "type": "payment_required",
                "title": "Payment Required Error",
            },
        ],
    },
)

RESPONSE_ACCESS_DENIED = httpx.Response(
    403,
    json={
        "errors": [
            {
                "type": "access_denied",
                "title": "Access Denied Error",
            },
        ],
    },
)

RESPONSE_INTERNAL_ERROR = httpx.Response(
    500,
    json={
        "errors": [
            {
                "type": "internal_error",
                "title": "Internal Error",
            },
        ],
    },
)
