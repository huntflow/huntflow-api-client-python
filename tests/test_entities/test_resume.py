from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import Resume
from huntflow_api_client.models.request.resume import (
    ApplicantResumeUpdateData,
    ApplicantResumeUpdateRequest,
)
from huntflow_api_client.models.response.resume import (
    ApplicantResumeResponse,
    ApplicantSourcesResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
APPLICANT_ID = 2
EXTERNAL_ID = 2

RESUME_SOURCES_RESPONSE: Dict[str, Any] = {
    "items": [
        {"id": 1, "foreign": "TS1", "name": "TestSource1", "type": "system"},
        {"id": 2, "foreign": "TS2", "name": "TestSource2", "type": "system"},
        {"id": 3, "foreign": "TS3", "name": "TestSource3", "type": "system"},
    ],
}

APPLICANT_RESUME_RESPONSE: Dict[str, Any] = {
    "id": 1,
    "auth_type": "AuthType",
    "account_source": 10,
    "updated": "2020-01-01T00:00:00+03:00",
    "created": "2020-01-01T00:00:00+03:00",
    "files": [
        {
            "id": 19,
            "url": "http://example.com",
            "content_type": "application/pdf",
            "name": "Resume.pdf",
        },
    ],
    "source_url": "string",
    "foreign": "580ab9e3ff02cd5e710039ed1f74593273674e",
    "key": "580ab9e3ff02cd5e710039ed1f74593273674e",
    "portfolio": [
        {
            "small": "https://example.com/image_small.png",
            "large": "https://example.com/image_large.png",
            "description": "Example image",
        },
    ],
    "data": {"body": "My resume"},
    "resume": {
        "personal_info": {
            "photo": {
                "small": "https://example.com/image_small.png",
                "medium": "https://example.com/image_medium.png",
                "large": "https://example.com/image_large.png",
                "external_id": "12",
                "description": "Applicant's photo",
                "source": "https://example.com/photo_source.png",
                "id": 10,
            },
            "first_name": "John",
            "middle_name": "Abraham",
            "last_name": "Doe",
            "birth_date": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
            "text_block": {"header": "About header", "body": "About body"},
        },
        "source_url": "https://example.com/resume",
        "position": "Manager",
        "specialization": [{"id": 14, "external_id": "100", "name": "Entity"}],
        "skill_set": ["English language"],
        "gender": {"id": 14, "external_id": "100", "name": "Entity"},
        "experience": [
            {
                "position": "Manager",
                "date_from": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                "date_to": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                "company": "Company",
                "url": "https://example.com",
                "area": {
                    "country": {"id": 14, "external_id": "100", "name": "Entity"},
                    "city": {"id": 14, "external_id": "100", "name": "Entity"},
                    "metro": {"id": 14, "external_id": "100", "name": "Entity"},
                    "address": "Washington DC",
                    "lat": 38.8951,
                    "lng": -77.0364,
                },
                "industries": [{"id": 14, "external_id": "100", "name": "Entity"}],
                "description": "I worked as a manager",
                "skills": [{"title": "English language"}],
            },
        ],
        "education": {
            "level": {"id": 14, "external_id": "100", "name": "Entity"},
            "higher": [
                {
                    "name": "Higher",
                    "description": "I have a higher education",
                    "date_from": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "date_to": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "area": {
                        "country": {"id": 14, "external_id": "100", "name": "Entity"},
                        "city": {"id": 14, "external_id": "100", "name": "Entity"},
                        "metro": {"id": 14, "external_id": "100", "name": "Entity"},
                        "address": "Washington DC",
                        "lat": 38.8951,
                        "lng": -77.0364,
                    },
                    "faculty": "Mathematics",
                    "form": {"id": 14, "external_id": "100", "name": "Entity"},
                },
            ],
            "vocational": [
                {
                    "name": "Higher",
                    "description": "I have a higher education",
                    "date_from": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "date_to": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "area": {
                        "country": {"id": 14, "external_id": "100", "name": "Entity"},
                        "city": {"id": 14, "external_id": "100", "name": "Entity"},
                        "metro": {"id": 14, "external_id": "100", "name": "Entity"},
                        "address": "Washington DC",
                        "lat": 38.8951,
                        "lng": -77.0364,
                    },
                    "faculty": "Mathematics",
                    "form": {"id": 14, "external_id": "100", "name": "Entity"},
                },
            ],
            "elementary": [
                {
                    "name": "Higher",
                    "description": "I have a higher education",
                    "date_from": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "date_to": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "area": {
                        "country": {"id": 14, "external_id": "100", "name": "Entity"},
                        "city": {"id": 14, "external_id": "100", "name": "Entity"},
                        "metro": {"id": 14, "external_id": "100", "name": "Entity"},
                        "address": "Washington DC",
                        "lat": 38.8951,
                        "lng": -77.0364,
                    },
                },
            ],
            "additional": [
                {
                    "name": "Higher",
                    "description": "I have a higher education",
                    "date_from": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "date_to": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "area": {
                        "country": {"id": 14, "external_id": "100", "name": "Entity"},
                        "city": {"id": 14, "external_id": "100", "name": "Entity"},
                        "metro": {"id": 14, "external_id": "100", "name": "Entity"},
                        "address": "Washington DC",
                        "lat": 38.8951,
                        "lng": -77.0364,
                    },
                    "result": "Completed",
                },
            ],
            "attestation": [
                {
                    "date": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                    "name": "string",
                    "organization": "string",
                    "description": "string",
                    "result": "string",
                },
            ],
        },
        "certificate": [
            {
                "name": "Certificate",
                "organization": "Certificate organnization",
                "description": "Certificate for John Doe",
                "url": "https://example.com/certificate_john_doe.pdf",
                "area": {
                    "country": {"id": 14, "external_id": "100", "name": "Entity"},
                    "city": {"id": 14, "external_id": "100", "name": "Entity"},
                    "metro": {"id": 14, "external_id": "100", "name": "Entity"},
                    "address": "Washington DC",
                    "lat": 38.8951,
                    "lng": -77.0364,
                },
                "date": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
            },
        ],
        "portfolio": [
            {
                "small": "https://example.com/image_small.png",
                "medium": "https://example.com/image_medium.png",
                "large": "https://example.com/image_large.png",
                "external_id": "12",
                "description": "Applicant's photo",
                "source": "https://example.com/photo_source.png",
                "id": 10,
            },
        ],
        "contact": [
            {
                "type": {"id": 14, "external_id": "100", "name": "Entity"},
                "value": "89999999999",
                "preferred": "true",
                "full_value": {
                    "country": "string",
                    "city": "string",
                    "number": "string",
                    "formatted": "string",
                },
            },
        ],
        "area": {
            "country": {"id": 14, "external_id": "100", "name": "Entity"},
            "city": {"id": 14, "external_id": "100", "name": "Entity"},
            "metro": {"id": 14, "external_id": "100", "name": "Entity"},
            "address": "Washington DC",
            "lat": 38.8951,
            "lng": -77.0364,
        },
        "relocation": {
            "type": {"id": 14, "external_id": "100", "name": "Entity"},
            "area": [
                {
                    "country": {"id": 14, "external_id": "100", "name": "Entity"},
                    "city": {"id": 14, "external_id": "100", "name": "Entity"},
                    "metro": {"id": 14, "external_id": "100", "name": "Entity"},
                    "address": "Washington DC",
                    "lat": 38.8951,
                    "lng": -77.0364,
                },
            ],
        },
        "citizenship": [{"id": 14, "external_id": "100", "name": "Entity"}],
        "work_permit": [{"id": 14, "external_id": "100", "name": "Entity"}],
        "language": [{"id": 14, "external_id": "100", "name": "Entity"}],
        "wanted_salary": {"amount": 0, "currency": "string"},
        "work_schedule": [{"id": 14, "external_id": "100", "name": "Entity"}],
        "business_trip_readiness": {"id": 14, "external_id": "100", "name": "Entity"},
        "recommendations": [
            {
                "value": "string",
                "date": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                "name": "string",
                "position": "Manager",
                "organization": "Test organization",
                "contact": "89999999999",
            },
        ],
        "has_vehicle": "false",
        "driver_license_types": ["A1", "B1"],
        "military": [
            {
                "date_from": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                "date_to": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
                "area": {
                    "country": {"id": 14, "external_id": "100", "name": "Entity"},
                    "city": {"id": 14, "external_id": "100", "name": "Entity"},
                    "metro": {"id": 14, "external_id": "100", "name": "Entity"},
                    "address": "Washington DC",
                    "lat": 38.8951,
                    "lng": -77.0364,
                },
                "unit": {"name": "Infantry", "external_id": 3336026},
            },
        ],
        "social_ratings": [
            {
                "kind": "string",
                "stats": "?",
                "tags": ["string"],
                "url": "string",
                "login": "string",
                "registered_at": "string",
            },
        ],
        "photos": [{"url": "string", "original": "string"}],
        "additionals": [{"name": "string", "description": "string"}],
        "wanted_place_of_work": "New York",
        "updated_on_source": {"year": 2021, "month": 12, "day": 12, "precision": "day"},
        "travel_time": {"id": 14, "external_id": "100", "name": "Entity"},
    },
}
GET_PDF_RESPONSE = bytes("pdf", "UTF-8")


async def test_get_resume_sources(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/sources",
        json=RESUME_SOURCES_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    resume = Resume(api_client)

    response = await resume.get_sources(ACCOUNT_ID)
    assert response == ApplicantSourcesResponse(**RESUME_SOURCES_RESPONSE)


async def test_get(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/externals/{EXTERNAL_ID}",
        json=APPLICANT_RESUME_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    resume = Resume(api_client)

    response = await resume.get(ACCOUNT_ID, APPLICANT_ID, EXTERNAL_ID)
    assert response == ApplicantResumeResponse(**APPLICANT_RESUME_RESPONSE)


async def test_delete_resume(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/externals/{EXTERNAL_ID}",
        status_code=204,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    resume = Resume(api_client)

    await resume.delete(ACCOUNT_ID, APPLICANT_ID, EXTERNAL_ID)


async def test_update(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/externals/{EXTERNAL_ID}",
        json=APPLICANT_RESUME_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    resume = Resume(api_client)

    data = ApplicantResumeUpdateRequest(
        account_source=10,
        data=ApplicantResumeUpdateData(body="My resume"),
    )

    response = await resume.update(ACCOUNT_ID, APPLICANT_ID, EXTERNAL_ID, data)
    assert response == ApplicantResumeResponse(**APPLICANT_RESUME_RESPONSE)


async def test_get_resume_pdf(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/"
        f"externals/{EXTERNAL_ID}/pdf",
        content=GET_PDF_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    resumes = Resume(api_client)

    response = await resumes.get_pdf(
        account_id=ACCOUNT_ID,
        applicant_id=APPLICANT_ID,
        external_id=EXTERNAL_ID,
    )
    assert response == GET_PDF_RESPONSE
