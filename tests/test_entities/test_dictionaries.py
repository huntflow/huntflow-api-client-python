from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.dictionaries import Dictionary
from huntflow_api_client.models.request.dictionaries import (
    DictionaryCreateRequest,
    DictionaryUpdateRequest,
)
from huntflow_api_client.models.response.dictionaries import (
    DictionariesListResponse,
    DictionaryResponse,
    DictionaryTaskResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
DICT_CODE = "dict_code"

DICT_GET_RESPONSE: Dict[str, Any] = {
    "id": 1,
    "code": DICT_CODE,
    "name": "Dict Name",
    "foreign": None,
    "created": "2023-05-02T09:18:28+03:00",
    "fields": [
        {
            "id": 7222,
            "name": "RU",
            "order": 0,
            "active": True,
            "parent": None,
            "deep": 0,
            "foreign": "Foreign",
            "meta": None,
        },
        {
            "id": 7223,
            "name": "Other",
            "order": 1,
            "active": True,
            "parent": None,
            "deep": 0,
            "foreign": "Other",
            "meta": None,
        },
    ],
}

DICT_LIST_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": 1,
            "code": "some_dict_code_1",
            "name": "Dict Name 1",
            "foreign": None,
            "created": "2022-05-02T09:18:24+03:00",
        },
        {
            "id": 2,
            "code": "some_dict_code_2",
            "name": "Dict Name 2",
            "foreign": None,
            "created": "2022-05-02T09:18:24+03:00",
        },
    ],
}

DICT_CREATE_REQUEST: Dict[str, Any] = {
    "code": DICT_CODE,
    "name": "Some Name",
    "foreign": "foreign",
    "items": [{"name": "item_name"}],
}

DICT_CREATE_RESPONSE = {
    "status": "ok",
    "payload": {"task_id": "111dd111-d1f0-1111-11d3-1ec4c87b1018"},
    "meta": {"data": {}, "account_id": 0},
}

DICT_UPDATE_REQUEST: Dict[str, Any] = {
    "name": "New Name",
    "items": [
        {
            "name": "New Name",
        },
    ],
}

DICT_UPDATE_RESPONSE = {
    "status": "ok",
    "payload": {"task_id": "111dd111-d1f0-1111-11d3-1ec4c87b1018"},
    "meta": {"data": {}, "account_id": 0},
}


async def test_get_dictionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/dictionaries/{DICT_CODE}",
        json=DICT_GET_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    dictionaries = Dictionary(api_client)

    response = await dictionaries.get(ACCOUNT_ID, DICT_CODE)
    assert response == DictionaryResponse.model_validate(DICT_GET_RESPONSE)


async def test_list_dictionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/dictionaries",
        json=DICT_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    dictionaries = Dictionary(api_client)

    response = await dictionaries.list(ACCOUNT_ID)
    assert response == DictionariesListResponse.model_validate(DICT_LIST_RESPONSE)


async def test_create_dictionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/dictionaries",
        json=DICT_CREATE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    dictionaries = Dictionary(api_client)

    api_request = DictionaryCreateRequest(**DICT_CREATE_REQUEST)
    response = await dictionaries.create(ACCOUNT_ID, api_request)
    assert response == DictionaryTaskResponse.model_validate(DICT_CREATE_RESPONSE)


async def test_update_dictionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/dictionaries/{DICT_CODE}",
        json=DICT_UPDATE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    dictionaries = Dictionary(api_client)

    api_request = DictionaryUpdateRequest(**DICT_UPDATE_REQUEST)
    response = await dictionaries.update(ACCOUNT_ID, DICT_CODE, api_request)
    assert response == DictionaryTaskResponse.model_validate(DICT_UPDATE_RESPONSE)
