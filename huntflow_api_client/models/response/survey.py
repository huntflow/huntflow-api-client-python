import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from huntflow_api_client.models.common import SurveyQuestionaryRespondentWithName
from huntflow_api_client.models.consts import SurveyType


class BaseSurveySchemaType(BaseModel):
    id: int = Field(..., description="Survey ID")
    name: str = Field(..., description="Survey name")
    type: SurveyType = Field(..., description="Type of survey")
    active: bool = Field(..., description="Is survey active?")
    created: datetime.datetime = Field(..., description="Date and time of creating a survey")
    updated: datetime.datetime = Field(
        ...,
        description="Date and time of the last update of the survey",
    )


class BaseSurveySchemaTypeWithSchemas(BaseSurveySchemaType):
    json_schema: dict = Field(..., alias="schema", description="JSON schema for the survey fields")
    ui_schema: dict = Field(..., description="UI schema for the survey fields")


class SurveySchemaTypeQResponse(BaseSurveySchemaTypeWithSchemas):
    type: SurveyType = Field(
        SurveyType.TYPE_Q,
        description="Type of survey",
        frozen=True,
    )
    title: Optional[str] = Field(..., description="Survey title")


class SurveySchemasTypeQListResponse(BaseModel):
    items: List[BaseSurveySchemaType] = Field(..., description="List of type q survey schemas")


class Creator(BaseModel):
    account_id: int = Field(..., description="Coworker ID")
    name: str = Field(..., description="Coworker name")


class SurveyQuestionaryCreatedInfo(BaseModel):
    id: int = Field(..., description="Survey questionary ID")
    created: datetime.datetime = Field(..., description="Date and time of creating a survey")
    created_by: Creator


class SurveyQuestionaryResponse(SurveyQuestionaryCreatedInfo):
    survey: SurveySchemaTypeQResponse = Field(..., description="Survey questionary schema")
    respondent: SurveyQuestionaryRespondentWithName
    survey_answer_id: Optional[int] = Field(
        ...,
        description="Survey questionary answer ID",
    )
    link: str = Field(..., description="Survey questionary link for applicant")


class SurveyQuestionaryAnswerResponse(BaseModel):
    id: int = Field(..., description="Survey questionary answer ID")
    created: datetime.datetime = Field(..., description="Date and time of creating an answer")
    survey: SurveySchemaTypeQResponse = Field(..., description="Survey questionary schema")
    respondent: SurveyQuestionaryRespondentWithName
    survey_questionary: SurveyQuestionaryCreatedInfo
    data: dict = Field(..., description="Answer data")


class SurveySchemasTypeAListResponse(BaseModel):
    items: List[BaseSurveySchemaType] = Field(..., description="List of type a survey schemas")


class SurveySchemaTypeAResponse(BaseSurveySchemaTypeWithSchemas):
    type: SurveyType = Field(
        SurveyType.TYPE_A,
        description="Type of survey",
        frozen=True,
    )


class SurveyTypeARespondent(BaseModel):
    account_id: int = Field(..., description="Account ID")
    name: str = Field(..., description="Name of the user who created the survey answer")


class SurveyAnswerTypeAResponse(BaseModel):
    id: int = Field(..., description="Survey answer of type A ID")
    created: datetime.datetime = Field(..., description="Date and time of creating an answer")
    survey: SurveySchemaTypeAResponse = Field(..., description="Survey schema")
    respondent: SurveyTypeARespondent = Field(..., description="Who created the survey answer")
    data: dict = Field(..., description="Answer data")
