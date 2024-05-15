from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.survey_type_a import SurveyTypeA
from huntflow_api_client.models.response.survey import (
    SurveyAnswerTypeAResponse,
    SurveySchemasTypeAListResponse,
    SurveySchemaTypeAResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL, VERSIONED_BASE_URL

ACCOUNT_ID = 1

SURVEY_FEEDBACK_SCHEMAS_LIST_RESPONSE = {
    "items": [
        {
            "id": 1,
            "name": "test_survey",
            "type": "type_a",
            "active": True,
            "created": "2020-01-01T00:00:00+03:00",
            "updated": "2020-01-01T00:00:00+03:00",
        },
    ],
}

SURVEY_FEEDBACK_SCHEMA_RESPONSE = {
    "id": 1,
    "name": "test_survey",
    "type": "type_a",
    "active": True,
    "created": "2020-01-01T00:00:00+03:00",
    "updated": "2020-01-01T00:00:00+03:00",
    "schema": {},
    "ui_schema": {},
}

SURVEY_ANSWER_RESPONSE = {
    "id": 1,
    "created": "2020-01-01T00:00:00+03:00",
    "survey": {
        "id": 1,
        "name": "test_survey",
        "type": "type_a",
        "active": True,
        "created": "2020-01-01T00:00:00+03:00",
        "updated": "2020-01-01T00:00:00+03:00",
        "schema": {},
        "ui_schema": {},
    },
    "respondent": {"account_id": 1, "name": "John Joe"},
    "data": {},
}


async def test_list(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_a?active=true",
        json=SURVEY_FEEDBACK_SCHEMAS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    feedback = SurveyTypeA(api_client)

    response = await feedback.list(ACCOUNT_ID)
    assert response == SurveySchemasTypeAListResponse.model_validate(
        SURVEY_FEEDBACK_SCHEMAS_LIST_RESPONSE,
    )


async def test_get(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    survey_id = 1
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_a/{survey_id}",
        json=SURVEY_FEEDBACK_SCHEMA_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    feedback = SurveyTypeA(api_client)

    response = await feedback.get(ACCOUNT_ID, survey_id)
    assert response == SurveySchemaTypeAResponse.model_validate(
        SURVEY_FEEDBACK_SCHEMA_RESPONSE,
    )


async def test_get_applicant_answer(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    survey_id = 1
    answer_id = 2
    httpx_mock.add_response(
        url=f"{VERSIONED_BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_a/"
        f"{survey_id}/answers/{answer_id}",
        json=SURVEY_ANSWER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    feedback = SurveyTypeA(api_client)

    response = await feedback.get_applicant_answer(ACCOUNT_ID, survey_id, answer_id)
    assert response == SurveyAnswerTypeAResponse.model_validate(
        SURVEY_ANSWER_RESPONSE,
    )
