import pytest
from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.errors import (
    AccessDeniedError,
    ApiError,
    BadRequestError,
    Error,
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
    NotFoundError,
    PaymentRequiredError,
    TokenExpiredError,
    TooManyRequestsError,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL


@pytest.fixture()
def api_client(token_proxy: HuntflowTokenProxy) -> HuntflowAPI:
    return HuntflowAPI(BASE_URL, token_proxy=token_proxy)


class TestErrorHandler401:
    url = f"{BASE_URL}/me"

    async def test_authorization_error(
        self,
        httpx_mock: HTTPXMock,
        api_client: HuntflowAPI,
    ) -> None:
        httpx_mock.add_response(
            url=self.url,
            method="GET",
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
        with pytest.raises(InvalidAccessTokenError) as exc:
            await api_client.request("GET", "/me")

        assert exc.value.code == 401
        assert exc.value.errors == [
            Error(
                type="authorization_error",
                title="Authorization Error",
                detail="Invalid access token",
            ),
        ]

    async def test_token_expired_error(
        self,
        httpx_mock: HTTPXMock,
        api_client: HuntflowAPI,
    ) -> None:
        httpx_mock.add_response(
            url=self.url,
            method="GET",
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
        with pytest.raises(TokenExpiredError) as exc:
            await api_client.request("GET", "/me")

        assert exc.value.code == 401
        assert exc.value.errors == [
            Error(
                type="authorization_error",
                title="Authorization Error",
                detail="token_expired",
            ),
        ]


class TestErrorHandler400:
    url = f"{BASE_URL}/accounts/11/vacancies"

    async def test_bad_request_error(self, httpx_mock: HTTPXMock, api_client: HuntflowAPI) -> None:
        httpx_mock.add_response(
            url=self.url,
            method="POST",
            status_code=400,
            json={
                "errors": [
                    {
                        "type": "value_error.missing",
                        "title": "field required",
                        "location": {"entity": "body", "variable": "/account_division"},
                    },
                    {
                        "type": "value_error.missing",
                        "title": "field required",
                        "location": {"entity": "body", "variable": "/account_region"},
                    },
                ],
            },
        )
        with pytest.raises(BadRequestError) as exc:
            await api_client.request("POST", "/accounts/11/vacancies", json={"position": "Test"})

        assert exc.value.code == 400
        assert exc.value.errors == [
            Error(
                type="value_error.missing",
                title="field required",
                location={"entity": "body", "variable": "/account_division"},
            ),
            Error(
                type="value_error.missing",
                title="field required",
                location={"entity": "body", "variable": "/account_region"},
            ),
        ]


class TestErrorHandler402:
    url = f"{BASE_URL}/me"

    async def test_payment_required_error(
        self,
        httpx_mock: HTTPXMock,
        api_client: HuntflowAPI,
    ) -> None:
        httpx_mock.add_response(
            url=self.url,
            method="GET",
            status_code=402,
            json={"errors": [{"type": "payment_required", "title": "Payment Required Error"}]},
        )
        with pytest.raises(PaymentRequiredError) as exc:
            await api_client.request("GET", "/me")

        assert exc.value.code == 402
        assert exc.value.errors == [Error(type="payment_required", title="Payment Required Error")]


class TestErrorHandler403:
    url = f"{BASE_URL}/me"

    async def test_access_denied_error(
        self,
        httpx_mock: HTTPXMock,
        api_client: HuntflowAPI,
    ) -> None:
        httpx_mock.add_response(
            url=self.url,
            method="GET",
            status_code=403,
            json={"errors": [{"type": "access_denied", "title": "Access Denied Error"}]},
        )
        with pytest.raises(AccessDeniedError) as exc:
            await api_client.request("GET", "/me")

        assert exc.value.code == 403
        assert exc.value.errors == [Error(type="access_denied", title="Access Denied Error")]


class TestErrorHandler404:
    async def test_not_found_error(self, httpx_mock: HTTPXMock, api_client: HuntflowAPI) -> None:
        httpx_mock.add_response(
            url=f"{BASE_URL}/accounts/11/vacancy_requests/0",
            method="GET",
            status_code=404,
            json={"errors": [{"type": "not_found", "title": "Unknown vacancy request"}]},
        )
        with pytest.raises(NotFoundError) as exc:
            await api_client.request("GET", "/accounts/11/vacancy_requests/0")

        assert exc.value.code == 404
        assert exc.value.errors == [Error(type="not_found", title="Unknown vacancy request")]

    async def test_invalid_refresh_token_error(
        self,
        httpx_mock: HTTPXMock,
        api_client: HuntflowAPI,
    ) -> None:
        httpx_mock.add_response(
            url=f"{BASE_URL}/token/refresh",
            method="POST",
            status_code=404,
            json={"errors": [{"type": "not_found", "title": "error.robot_token.not_found"}]},
        )
        with pytest.raises(InvalidRefreshTokenError) as exc:
            await api_client.request("POST", "/token/refresh", json={"refresh_token": "123"})

        assert exc.value.code == 404
        assert exc.value.errors == [Error(type="not_found", title="error.robot_token.not_found")]


class TestErrorHandler429:
    url = f"{BASE_URL}/me"

    async def test_too_many_requests_error(
        self,
        httpx_mock: HTTPXMock,
        api_client: HuntflowAPI,
    ) -> None:
        httpx_mock.add_response(
            url=self.url,
            method="GET",
            status_code=429,
            json={
                "errors": [
                    {
                        "type": "too_many_requests",
                        "title": "Answer request created too frequently",
                    },
                ],
            },
        )
        with pytest.raises(TooManyRequestsError) as exc:
            await api_client.request("GET", "/me")

        assert exc.value.code == 429
        assert exc.value.errors == [
            Error(type="too_many_requests", title="Answer request created too frequently"),
        ]


class TestDefaultErrorHandler:
    url = f"{BASE_URL}/me"

    async def test_api_error(self, httpx_mock: HTTPXMock, api_client: HuntflowAPI) -> None:
        httpx_mock.add_response(
            url=self.url,
            method="GET",
            status_code=500,
            json={"errors": [{"type": "internal_error", "title": "Internal Error"}]},
        )
        with pytest.raises(ApiError) as exc:
            await api_client.request("GET", "/me")

        assert exc.value.code == 500
        assert exc.value.errors == [Error(type="internal_error", title="Internal Error")]
