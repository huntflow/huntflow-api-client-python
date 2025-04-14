from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin, ListEntityMixin
from huntflow_api_client.models.response.survey import (
    SurveyAnswerTypeAResponse,
    SurveySchemasTypeAListResponse,
    SurveySchemaTypeAResponse,
)


class SurveyTypeA(BaseEntity, GetEntityMixin, ListEntityMixin):
    async def list(
        self,
        account_id: int,
        active: bool = True,
    ) -> SurveySchemasTypeAListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/surveys/type_a

        :param account_id: Organization ID
        :param active: Shows only active schemas
        :return: List of all applicant feedback forms in organization.
        """
        params = {"active": active}
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/surveys/type_a",
            params=params,
        )
        return SurveySchemasTypeAListResponse.model_validate(response.json())

    async def get(self, account_id: int, survey_id: int) -> SurveySchemaTypeAResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/surveys/type_a/-survey_id-

        :param account_id: Organization ID
        :param survey_id: Survey ID
        :return: An applicant feedback forms in organization.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/surveys/type_a/{survey_id}",
        )
        return SurveySchemaTypeAResponse.model_validate(response.json())

    async def get_applicant_answer(
        self,
        account_id: int,
        survey_id: int,
        answer_id: int,
    ) -> SurveyAnswerTypeAResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/surveys/type_a/-survey_id-/answers/-answer_id-

        :param account_id: Organization ID
        :param survey_id: Survey ID
        :param answer_id: Answer ID
        :return: Returns answer of applicant feedback form.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/surveys/type_a/{survey_id}/answers/{answer_id}",
        )
        return SurveyAnswerTypeAResponse.model_validate(response.json())
