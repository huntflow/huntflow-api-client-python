from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.applicant_offers import ApplicantOffer
from huntflow_api_client.models.request.applicant_offers import ApplicantOfferUpdate
from huntflow_api_client.models.response.applicant_offers import ApplicantVacancyOfferResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
OFFER_ID = 2
APPLICANT_ID = 3
VACANCY_FRAME_ID = 4

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


async def test_update(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/offers/{OFFER_ID}",
        json=OFFER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = ApplicantOffer(api_client)
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
        f"/vacancy_frames/{VACANCY_FRAME_ID}/offer?normalize=false",
        json=OFFER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = ApplicantOffer(api_client)

    response = await offers.get(
        account_id=ACCOUNT_ID,
        applicant_id=APPLICANT_ID,
        vacancy_frame_id=VACANCY_FRAME_ID,
    )
    assert response == ApplicantVacancyOfferResponse(**OFFER_RESPONSE)


async def test_get_offer_pdf(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/offers/{OFFER_ID}/pdf",
        content=GET_PDF_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    offers = ApplicantOffer(api_client)

    response = await offers.get_pdf(
        account_id=ACCOUNT_ID,
        applicant_id=APPLICANT_ID,
        offer_id=OFFER_ID,
    )
    assert response == GET_PDF_RESPONSE
