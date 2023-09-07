from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import ApplicantLog
from huntflow_api_client.models.consts import ApplicantLogType
from huntflow_api_client.models.request.applicant_logs import CreateApplicantLogRequest
from huntflow_api_client.models.response.applicant_logs import (
    ApplicantLogResponse,
    CreateApplicantLogResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
APPLICANT_ID = 2
VACANCY_ID = 3

APPLICANT_LOG_LIST_RESPONSE = {
    "page": 1,
    "count": 30,
    "total_pages": 2,
    "total_items": 50,
    "items": [
        {
            "id": 20,
            "type": "ADD",
            "vacancy": 14,
            "status": 13,
            "source": "326784718",
            "rejection_reason": 8,
            "created": "2020-01-01T00:00:00+03:00",
            "employment_date": "2020-01-01",
            "account_info": {"id": 9, "name": "John Joe"},
            "comment": "Example comment",
            "files": [
                {
                    "id": 19,
                    "url": "http://example.com",
                    "content_type": "application/pdf",
                    "name": "Resume.pdf",
                },
            ],
            "calendar_event": {
                "id": 1,
                "name": "Event: Interview John Doe",
                "all_day": False,
                "created": "2020-01-01T00:00:00+03:00",
                "creator": {"displayName": "John Doe", "email": "test@example.com", "self": False},
                "description": "Interview with John Doe",
                "timezone": "Europe/Moscow",
                "start": "2020-01-01T00:00:00+03:00",
                "end": "2020-01-01T00:00:00+03:00",
                "etag": "<etag_value>",
                "event_type": "interview",
                "interview_type": 17,
                "calendar": 4,
                "vacancy": 2,
                "foreign": "f1",
                "location": "Washington street 121",
                "attendees": [
                    {
                        "member": 10,
                        "displayName": "John Doe",
                        "email": "test@example.com",
                        "responseStatus": "confirmed",
                    },
                ],
                "reminders": [{"method": "popup", "minutes": 10}],
                "status": "tentative",
                "transparency": "busy",
                "recurrence": [
                    None,
                ],
            },
            "hired_in_fill_quota": {
                "id": 2,
                "vacancy_frame": 5,
                "vacancy_request": 3,
                "created": "2020-01-01T00:00:00+03:00",
                "changed": "2020-01-01T00:00:00+03:00",
                "applicants_to_hire": 10,
                "already_hired": 8,
                "deadline": "1970-01-01",
                "closed": "2020-01-01T00:00:00+03:00",
                "work_days_in_work": 5,
                "work_days_after_deadline": 4,
                "account_info": {"id": 11, "name": "John Joe", "email": "test@example.com"},
            },
            "applicant_offer": {
                "id": 1,
                "account_applicant_offer": 1,
                "created": "2020-01-01T00:00:00+03:00",
            },
            "email": {
                "id": 1,
                "created": "2020-01-01T00:00:00+03:00",
                "subject": "Welcome aboard!",
                "email_thread": 15,
                "account_email": 6,
                "files": [
                    {
                        "id": 19,
                        "url": "http://example.com",
                        "content_type": "application/pdf",
                        "name": "Resume.pdf",
                    },
                ],
                "foreign": "f1",
                "timezone": "Europe/Moscow",
                "html": "<p>Hello John!</p>",
                "from_email": "sender@example.com",
                "from_name": "John Doe",
                "replyto": ["<CAOFTTcsSJ76SbpbHwDxA8MUrSZjcgb+X39TL_G9n01UEuBDOAA@mail.gmail.com>"],
                "send_at": "2020-01-01T00:00:00+03:00",
                "to": [{"type": "cc", "displayName": "John Doe", "email": "email@example.com"}],
                "state": "QUEUED",
            },
            "survey_questionary": {
                "id": 1,
                "survey": {
                    "id": 1,
                    "name": "test_survey",
                    "type": "type_a",
                    "active": True,
                    "created": "2020-01-01T00:00:00+03:00",
                    "updated": "2020-01-01T00:00:00+03:00",
                    "title": "Type R title",
                },
                "survey_answer_id": 1,
                "created": "2020-01-01T00:00:00+03:00",
            },
        },
    ],
}
APPLICANT_CREATE_LOG_RESPONSE: Dict[str, Any] = {
    "id": 1,
    "applicant": APPLICANT_ID,
    "type": "COMMENT",
    "vacancy": None,
    "status": None,
    "rejection_reason": None,
    "created": "2023-06-09T11:41:10+03:00",
    "employment_date": None,
    "applicant_offer": None,
    "comment": "Example comment",
    "files": [],
    "calendar_event": None,
    "email": None,
    "survey_questionary": None,
    "survey_answer_of_type_a": None,
    "data": None,
    "source": None,
    "workdays_after_deadline_for_employment_date": None,
    "group_action": None,
    "vacancy_frame": None,
    "removed": None,
    "work_days_in_work": None,
    "recruitment_evaluation": None,
    "work_days_after_deadline": None,
    "sms": None,
    "account": ACCOUNT_ID,
    "phone_call": None,
    "im": [],
    "hired_in_fill_quota": None,
    "workdays_until_employment_date": None,
}


async def test_applicant_log_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/logs?"
        f"vacancy={VACANCY_ID}&&type={ApplicantLogType.ADD.value}&&personal=true"
        f"&&page=1&&count=30&&personal=false",
        status_code=200,
        json=APPLICANT_LOG_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    logs = ApplicantLog(api_client)

    response = await logs.list(
        account_id=ACCOUNT_ID,
        applicant_id=APPLICANT_ID,
        vacancy=VACANCY_ID,
        type_=ApplicantLogType.ADD,
        personal=True,
    )
    assert response == ApplicantLogResponse.model_validate(APPLICANT_LOG_LIST_RESPONSE)


async def test_create_log(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/applicants/{APPLICANT_ID}/logs",
        status_code=200,
        json=APPLICANT_CREATE_LOG_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    logs = ApplicantLog(api_client)
    data = CreateApplicantLogRequest(comment="Example comment")
    response = await logs.create(
        account_id=ACCOUNT_ID,
        applicant_id=APPLICANT_ID,
        data=data,
    )
    assert response == CreateApplicantLogResponse.model_validate(APPLICANT_CREATE_LOG_RESPONSE)
