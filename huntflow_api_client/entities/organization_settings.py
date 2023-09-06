from huntflow_api_client.entities.base import BaseEntity
from huntflow_api_client.models.response.organization_settings import (
    BaseSurveySchemaTypeWithSchemas,
    CloseReasonsListResponse,
    HoldReasonsListResponse,
)


class OrganizationSettings(BaseEntity):
    async def get_hold_reasons(self, account_id: int) -> HoldReasonsListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancy_hold_reasons

        :param account_id: Organization ID
        :return: List of vacancy hold reasons
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/vacancy_hold_reasons",
        )
        return HoldReasonsListResponse.model_validate(response.json())

    async def get_close_reasons(self, account_id: int) -> CloseReasonsListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancy_close_reasons

        :param account_id: Organization ID
        :return: List of vacancy close reasons
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/vacancy_close_reasons",
        )
        return CloseReasonsListResponse.model_validate(response.json())

    async def get_applicant_survey_form(
        self,
        account_id: int,
        survey_id: int,
    ) -> BaseSurveySchemaTypeWithSchemas:
        """
        API method reference
           https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/surveys/type_a/-survey_id-

        :param account_id: Organization ID
        :param survey_id: Survey ID
        :return: An applicant survey form
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/surveys/type_a/{survey_id}",
        )
        return BaseSurveySchemaTypeWithSchemas.model_validate(response.json())
