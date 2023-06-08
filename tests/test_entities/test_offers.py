from typing import Dict
from typing import Any

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.offers import Offer
from huntflow_api_client.models.request.offers import ApplicantOfferUpdate
from huntflow_api_client.models.response.offers import (
    AccountOffersListResponse,
    AccountOfferResponse,
    ApplicantVacancyOfferResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
OFFER_ID = 2
APPLICANT_ID = 3
VACANCY_FRAME_ID = 4

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
OFFER_RESPONSE: Dict[str, Any] = {
    "id": 1,
    "account_applicant_offer": 1,
    "created": "2020-01-01T00:00:00+03:00",
    "values": {
        "whom_name": "Doe John Hovard",
        "position_name": "CTO",
        "whom_date": "24.11.2021",
        "offer_text": "<p>Welcome to our company!</p>",
    },
}

GET_PDF_RESPONSE = bytes("pdf", "UTF-8")


async def test_get_current_user(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/offers",
        json=GET_ORG_OFFERS_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = Offer(api_client)

    response = await offers.get_account_offers(account_id=ACCOUNT_ID)
    assert response == AccountOffersListResponse(**GET_ORG_OFFERS_RESPONSE)


async def test_get_account_offers_with_schema(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/offers/{OFFER_ID}",
        json=GET_ORG_OFFERS_WITH_SCHEMA_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = Offer(api_client)

    response = await offers.get_account_offers_with_schema(account_id=ACCOUNT_ID, offer_id=OFFER_ID)
    assert response == AccountOfferResponse(**GET_ORG_OFFERS_WITH_SCHEMA_RESPONSE)


async def test_update(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/offers/{OFFER_ID}",
        json=OFFER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = Offer(api_client)
    data = ApplicantOfferUpdate(
        account_applicant_offer=1,
        values={
            "position_name": "CTO",
            "offer_text": "<p>Welcome to our company!</p>",
            "whom_date": "2021-11-24",
            "whom_name": "Doe John Hovard",
        },
    )

    response = await offers.update(
        account_id=ACCOUNT_ID,
        applicant_id=APPLICANT_ID,
        offer_id=OFFER_ID,
        data=data,
    )
    assert response == ApplicantVacancyOfferResponse(**OFFER_RESPONSE)


async def test_get_applicant_on_vacancy_offer(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}"
        f"/vacancy_frames/{VACANCY_FRAME_ID}/offer",
        json=OFFER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = Offer(api_client)

    response = await offers.get_applicant_on_vacancy_offer(
        account_id=ACCOUNT_ID, applicant_id=APPLICANT_ID, vacancy_frame_id=VACANCY_FRAME_ID,
    )
    assert response == ApplicantVacancyOfferResponse(**OFFER_RESPONSE)


async def test_get_pdf(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/offers/{OFFER_ID}/pdf",
        content=GET_PDF_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = Offer(api_client)

    response = await offers.get_pdf(
        account_id=ACCOUNT_ID, applicant_id=APPLICANT_ID, offer_id=OFFER_ID,
    )
    assert response == GET_PDF_RESPONSE
