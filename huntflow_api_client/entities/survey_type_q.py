from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    DeleteEntityMixin,
    GetEntityMixin,
)
from huntflow_api_client.models.request.survey import SurveyQuestionaryCreateRequest
from huntflow_api_client.models.response.survey import (
    SurveyQuestionaryAnswerResponse,
    SurveyQuestionaryResponse,
    SurveySchemasTypeQListResponse,
    SurveySchemaTypeQResponse,
)


class SurveyTypeQ(
    BaseEntity,
    GetEntityMixin,
    CreateEntityMixin,
    DeleteEntityMixin,
):
    async def list_schemas(
        self,
        account_id: int,
        active: bool = True,
    ) -> SurveySchemasTypeQListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/surveys/type_q

        :param account_id: Organization ID
        :param active: Shows only active schemas
        :return: List of all survey questionary schemas for applicants for organization.
        """
        params = {"active": active}
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/surveys/type_q",
            params=params,
        )
        return SurveySchemasTypeQListResponse.model_validate(response.json())

    async def get_schema(self, account_id: int, survey_id: int) -> SurveySchemaTypeQResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/surveys/type_q/-survey_id-

        :param account_id: Organization ID
        :param survey_id: Survey ID
        :return: Survey questionary schema for applicants.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/surveys/type_q/{survey_id}",
        )
        return SurveySchemaTypeQResponse.model_validate(response.json())

    async def create(
        self,
        account_id: int,
        request_data: SurveyQuestionaryCreateRequest,
    ) -> SurveyQuestionaryResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/surveys/type_q/questionaries

        :param account_id: Organization ID
        :param request_data: Request body structure
        :return: Survey questionary for applicants.
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/surveys/type_q/questionaries",
            data=request_data.jsonable_dict(),
        )
        return SurveyQuestionaryResponse.model_validate(response.json())

    async def get(self, account_id: int, questionary_id: int) -> SurveyQuestionaryResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/surveys/type_q/questionaries/-questionary_id-

        :param account_id: Organization ID
        :param questionary_id: Survey questionary ID
        :return: Survey
        questionary for applicants.
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/surveys/type_q/questionaries/{questionary_id}",
        )
        return SurveyQuestionaryResponse.model_validate(response.json())

    async def delete(self, account_id: int, questionary_id: int) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/surveys/type_q/questionaries/-questionary_id-

        :param account_id: Organization ID
        :param questionary_id: Survey questionary ID
        """
        await self._api.request(
            "DELETE",
            f"/accounts/{account_id}/surveys/type_q/questionaries/{questionary_id}",
        )

    async def get_answer(self, account_id: int, answer_id: int) -> SurveyQuestionaryAnswerResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/surveys/type_q/answers/-answer_id-

        :param account_id: Organization ID
        :param answer_id: Survey questionary answer ID
        :return: Survey questionary answer
        """

        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/surveys/type_q/answers/{answer_id}",
        )
        return SurveyQuestionaryAnswerResponse.model_validate(response.json())
