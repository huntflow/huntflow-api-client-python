from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.account_offers import AccountOffer
from huntflow_api_client.models.response.account_offers import (
    AccountOfferResponse,
    AccountOffersListResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
OFFER_ID = 2

GET_ORG_OFFERS_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": 100,
            "name": "Standard offer",
            "active": True,
            "template": "<!doctype html>\n<html>\n<head>\n    "
            '<meta charset="utf-8">\n</head>\n<body>\n'
            "{% set values = data.offer['values'] %}\n"
            "{% set applicant = data.applicant %}\n"
            '<div class="logo">\n    '
            "{% if data.account.photo %}\n        "
            '<img src="{{ data.account.photo }}">\n    '
            '{% endif %}\n</div>\n<div class="offer">\n   '
            ' <div class="offer__header">\n        '
            "Offer: {{ values.whom_name }}<br>\n        "
            "Position: {{ values.position_name }}<br>\n        "
            "Date of employment: {{ values.whom_date }}\n    "
            '</div>\n    <div class="offer__body">\n        '
            "{{ values.offer_text|safe }}\n    </div>\n    "
            '<div class="offer__footer">\n        <div>\n            '
            "{{ data.manager.name }}<br>\n            "
            "{% if data.manager.position %}\n                "
            "{{ data.manager.position }}<br>\n            "
            "{% endif %}\n        </div>\n    "
            "</div>\n</div>\n</body>\n</html>\n",
        },
    ],
}
GET_ORG_OFFERS_WITH_SCHEMA_RESPONSE: Dict[str, Any] = {
    "id": OFFER_ID,
    "name": "Standard offer",
    "active": True,
    "template": "<!doctype html>\n<html>\n<head>\n    "
    '<meta charset="utf-8">\n</head>\n<body>\n'
    "{% set values = data.offer['values'] %}\n"
    "{% set applicant = data.applicant %}\n"
    '<div class="logo">\n    '
    "{% if data.account.photo %}\n        "
    '<img src="{{ data.account.photo }}">\n    '
    '{% endif %}\n</div>\n<div class="offer">\n   '
    ' <div class="offer__header">\n        '
    "Offer: {{ values.whom_name }}<br>\n        "
    "Position: {{ values.position_name }}<br>\n        "
    "Date of employment: {{ values.whom_date }}\n    "
    '</div>\n    <div class="offer__body">\n        '
    "{{ values.offer_text|safe }}\n    </div>\n    "
    '<div class="offer__footer">\n        <div>\n            '
    "{{ data.manager.name }}<br>\n            "
    "{% if data.manager.position %}\n                "
    "{{ data.manager.position }}<br>\n            "
    "{% endif %}\n        </div>\n    "
    "</div>\n</div>\n</body>\n</html>\n",
    "schema": {
        "whom_name": {
            "type": "string",
            "title": "Whom name",
            "required": True,
            "order": 1,
            "id": 163,
            "value": True,
            "account": ACCOUNT_ID,
            "key": True,
            "value_from": ["applicant.last_name", "applicant.first_name", "applicant.middle_name"],
        },
        "position_name": {
            "type": "string",
            "title": "Position",
            "required": True,
            "order": 2,
            "id": 164,
            "value": True,
            "account": ACCOUNT_ID,
            "key": True,
            "value_from": "vacancy.position",
        },
        "whom_date": {
            "type": "date",
            "title": "Whom date",
            "required": True,
            "order": 3,
            "id": 165,
            "value": None,
            "account": ACCOUNT_ID,
            "key": None,
        },
        "offer_text": {
            "type": "html",
            "title": "Offer text",
            "required": True,
            "order": 4,
            "id": 166,
            "value": None,
            "account": ACCOUNT_ID,
            "key": None,
        },
    },
}


async def test_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/offers",
        json=GET_ORG_OFFERS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = AccountOffer(api_client)

    response = await offers.list(account_id=ACCOUNT_ID)
    assert response == AccountOffersListResponse(**GET_ORG_OFFERS_RESPONSE)


async def test_get(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/offers/{OFFER_ID}",
        json=GET_ORG_OFFERS_WITH_SCHEMA_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = AccountOffer(api_client)

    response = await offers.get(account_id=ACCOUNT_ID, offer_id=OFFER_ID)
    assert response == AccountOfferResponse(**GET_ORG_OFFERS_WITH_SCHEMA_RESPONSE)
