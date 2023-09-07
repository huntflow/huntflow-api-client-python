import uuid

import pytest
from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.divisions import AccountDivision
from huntflow_api_client.models.request.divisions import BatchDivisionsRequest
from huntflow_api_client.models.response.divisions import (
    BatchDivisionsResponse,
    DivisionsListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
COWORKER_ID = 1
ACCOUNT_DIVISIONS_LIST_RESPONSE = {
    "items": [
        {
            "id": 1,
            "name": "1",
            "order": 0,
            "active": True,
            "parent": None,
            "deep": 0,
            "foreign": "1",
            "meta": {},
        },
        {
            "id": 2,
            "name": "2",
            "order": 1,
            "active": True,
            "parent": None,
            "deep": 0,
            "foreign": "2",
            "meta": {},
        },
    ],
    "meta": {"levels": 1, "has_inactive": True},
}
BATCH_ACCOUNT_DIVISIONS_REQUEST = {
    "items": [
        {
            "name": "name",
            "foreign": "foreign",
            "items": [
                {
                    "name": "name2",
                    "foreign": "foreign2",
                },
            ],
        },
    ],
}
BATCH_ACCOUNT_DIVISIONS_RESPONSE = {
    "status": "ok",
    "payload": {
        "task_id": uuid.uuid4().hex,
    },
    "meta": {
        "data": {},
        "account_id": ACCOUNT_ID,
    },
}


async def test_list_account_division(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    only_available = True
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/divisions?only_available=true",
        json=ACCOUNT_DIVISIONS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    divisions = AccountDivision(api_client)

    response = await divisions.list(ACCOUNT_ID, only_available=only_available)
    assert response == DivisionsListResponse.model_validate(ACCOUNT_DIVISIONS_LIST_RESPONSE)

    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/coworkers/{COWORKER_ID}/divisions",
        json=ACCOUNT_DIVISIONS_LIST_RESPONSE,
    )
    response = await divisions.list(ACCOUNT_ID, COWORKER_ID)
    assert response == DivisionsListResponse.model_validate(ACCOUNT_DIVISIONS_LIST_RESPONSE)

    with pytest.raises(ValueError):
        await divisions.list(ACCOUNT_ID, 1, True)


async def test_create_account_division(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/divisions/batch",
        json=BATCH_ACCOUNT_DIVISIONS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    divisions = AccountDivision(api_client)
    create_divisions_request = BatchDivisionsRequest.model_validate(BATCH_ACCOUNT_DIVISIONS_REQUEST)
    response = await divisions.create(ACCOUNT_ID, create_divisions_request)
    assert response == BatchDivisionsResponse.model_validate(BATCH_ACCOUNT_DIVISIONS_RESPONSE)
