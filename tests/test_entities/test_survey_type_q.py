from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.survey_type_q import SurveyTypeQ
from huntflow_api_client.models.request.survey import SurveyQuestionaryCreateRequest
from huntflow_api_client.models.response.survey import (
    SurveyQuestionaryAnswerResponse,
    SurveyQuestionaryResponse,
    SurveySchemasTypeQListResponse,
    SurveySchemaTypeQResponse,
)
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1

SURVEY_QUESTIONARY_SCHEMAS_LIST_RESPONSE = {
    "items": [
        {
            "id": 28,
            "name": "test",
            "type": "type_q",
            "active": True,
            "created": "2023-09-08T17:24:11+03:00",
            "updated": "2023-09-08T17:24:11+03:00",
        },
    ],
}

SURVEY_QUESTIONARY_SCHEMA_RESPONSE = {
    "id": 28,
    "name": "test",
    "type": "type_q",
    "active": True,
    "created": "2023-09-08T17:24:11+03:00",
    "updated": "2023-09-08T17:24:11+03:00",
    "schema": {
        "type": "object",
        "required": [],
        "properties": {"nLfFauQOra_3hDAXJ3Gct": {"type": "string", "title": "text"}},
        "additionalProperties": False,
    },
    "ui_schema": {
        "ui:order": ["nLfFauQOra_3hDAXJ3Gct"],
        "nLfFauQOra_3hDAXJ3Gct": {
            "ui:widget": "TextWidget",
            "ui:description": "text",
            "ui:placeholder": "text",
        },
    },
    "title": "text",
}

APPLICANT_SURVEY_QUESTIONARY_RESPONSE = {
    "id": 1,
    "created": "2023-09-08T17:51:12+03:00",
    "created_by": {"account_id": 47, "name": "API: test"},
    "survey": {
        "id": 28,
        "name": "test",
        "type": "type_q",
        "active": True,
        "created": "2023-09-08T17:24:11+03:00",
        "updated": "2023-09-08T17:24:11+03:00",
        "schema": {
            "type": "object",
            "required": [],
            "properties": {"nLfFauQOra_3hDAXJ3Gct": {"type": "string", "title": "test"}},
            "additionalProperties": False,
        },
        "ui_schema": {
            "ui:order": ["nLfFauQOra_3hDAXJ3Gct"],
            "nLfFauQOra_3hDAXJ3Gct": {
                "ui:widget": "TextWidget",
                "ui:description": "text",
                "ui:placeholder": "text",
            },
        },
        "title": "text",
    },
    "respondent": {"applicant_id": 30, "name": "John Doe"},
    "survey_answer_id": None,
    "link": "https://huntflow.ai/",
}

SURVEY_QUESTIONARY_CREATE_REQUEST = {"survey_id": 28, "respondent": {"applicant_id": 30}}

SURVEY_QUESTIONARY_ANSWER_RESPONSE = {
    "id": 543,
    "created": "2023-02-02 12:34:56",
    "survey": {
        "title": "test",
        "name": "questionary",
        "id": 123,
        "type": "type_q",
        "active": True,
        "created": "2022-01-01 12:12:12",
        "updated": "2022-01-01 13:13:13",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": [],
            "properties": {
                "Xh6atn8xwSAt1i33jV4fZ": {
                    "type": "number",
                    "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    "title": "text",
                    "metadata": {
                        "files": [
                            {
                                "content_type": "image/jpeg",
                                "id": 77,
                                "name": "0.jpg",
                                "url": "https://huntflow.ai/file",
                            },
                        ],
                    },
                },
                "SdER2dgf5Fsddf6SfgZkG": {
                    "type": "array",
                    "title": "text",
                    "items": {"type": "number"},
                },
            },
        },
        "ui_schema": {
            "ui:order": ["Xh6atn8xwSAt1i33jV4fZ", "SdER2dgf5Fsddf6SfgZkG"],
            "Xh6atn8xwSAt1i33jV4fZ": {
                "ui:widget": "RatingRadioWidget",
                "ui:description": "text",
            },
            "SdER2dgf5Fsddf6SfgZkG": {
                "ui:widget": "AttachFileWidget",
                "ui:description": "text",
            },
        },
    },
    "respondent": {"applicant_id": 456, "name": "Applicant Name"},
    "survey_questionary": {
        "id": 732,
        "created": "2023-01-01 11:22:33",
        "created_by": {"account_id": 1, "name": "Creator Name"},
    },
    "data": {
        "Xh6atn8xwSAt1i33jV4fZ": 4,
        "SdER2dgf5Fsddf6SfgZkG": [
            {
                "content_type": "image/jpeg",
                "id": 98,
                "name": "2.jpg",
                "url": "https://huntflow.ai/uploads3",
            },
            {
                "content_type": "image/jpeg",
                "id": 99,
                "name": "3.jpg",
                "url": "https://huntflow.ai/uploads3/na",
            },
        ],
    },
}


async def test_list_schemas(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_q?active=true",
        json=SURVEY_QUESTIONARY_SCHEMAS_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = SurveyTypeQ(api_client)

    response = await questionary.list_schemas(ACCOUNT_ID)
    assert response == SurveySchemasTypeQListResponse.model_validate(
        SURVEY_QUESTIONARY_SCHEMAS_LIST_RESPONSE,
    )


async def test_get_schema(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    survey_id = 1
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_q/{survey_id}",
        json=SURVEY_QUESTIONARY_SCHEMA_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = SurveyTypeQ(api_client)

    response = await questionary.get_schema(ACCOUNT_ID, survey_id)
    assert response == SurveySchemaTypeQResponse.model_validate(
        SURVEY_QUESTIONARY_SCHEMA_RESPONSE,
    )


async def test_create_survey_questionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    request_data = SurveyQuestionaryCreateRequest.model_validate(SURVEY_QUESTIONARY_CREATE_REQUEST)
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_q/questionaries",
        json=APPLICANT_SURVEY_QUESTIONARY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = SurveyTypeQ(api_client)

    response = await questionary.create(ACCOUNT_ID, request_data=request_data)
    assert response == SurveyQuestionaryResponse.model_validate(
        APPLICANT_SURVEY_QUESTIONARY_RESPONSE,
    )


async def test_get_survey_questionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    questionary_id = 1
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_q/questionaries/{questionary_id}",
        json=APPLICANT_SURVEY_QUESTIONARY_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = SurveyTypeQ(api_client)

    response = await questionary.get(ACCOUNT_ID, questionary_id)
    assert response == SurveyQuestionaryResponse.model_validate(
        APPLICANT_SURVEY_QUESTIONARY_RESPONSE,
    )


async def test_delete_survey_questionary(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    questionary_id = 1
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_q/questionaries/{questionary_id}",
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = SurveyTypeQ(api_client)

    await questionary.delete(ACCOUNT_ID, questionary_id)


async def test_get_answer(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    answer_id = 1
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/surveys/type_q/answers/{answer_id}",
        json=SURVEY_QUESTIONARY_ANSWER_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    questionary = SurveyTypeQ(api_client)

    response = await questionary.get_answer(ACCOUNT_ID, answer_id)
    assert response == SurveyQuestionaryAnswerResponse.model_validate(
        SURVEY_QUESTIONARY_ANSWER_RESPONSE,
    )
