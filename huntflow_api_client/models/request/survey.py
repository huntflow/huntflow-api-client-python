from pydantic import Field

from huntflow_api_client.models.common import JsonRequestModel, SurveyQuestionaryRespondent


class SurveyQuestionaryCreateRequest(JsonRequestModel):
    survey_id: int = Field(..., description="Survey ID")
    respondent: SurveyQuestionaryRespondent
