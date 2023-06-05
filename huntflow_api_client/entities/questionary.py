from huntflow_api_client.entities.base import BaseEntity, CreateEntityMixin, GetEntityMixin
from huntflow_api_client.models.request.questionary import QuestionaryRequest
from huntflow_api_client.models.response.questionary import (
    QuestionaryResponse,
    QuestionarySchemaResponse,
)


class ApplicantsQuestionary(BaseEntity, GetEntityMixin, CreateEntityMixin):
    async def get_organization_questionary(self, account_id: int) -> QuestionarySchemaResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/questionary

        :param account_id: Organization ID

        :return: A schema of applicant's questionary for organization
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/applicants/questionary")
        return QuestionarySchemaResponse.parse_obj(response.json())

    async def create(
        self, account_id: int, applicant_id: int, data: QuestionaryRequest,
    ) -> QuestionaryResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/applicants/-applicant_id-/questionary

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param data: Questionary data depends on the questionary schema.

        :return: Return created questionary
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/applicants/{applicant_id}/questionary",
            json=data.jsonable_dict(exclude_none=True),
        )
        return QuestionaryResponse.parse_obj(response.json())

    async def get(self, account_id: int, applicant_id: int) -> QuestionaryResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/questionary

        :param account_id: Organization ID
        :param applicant_id: Applicant ID

        :return: A questionary for the specified applicant
        """
        response = await self._api.request(
            "GET", f"/accounts/{account_id}/applicants/{applicant_id}/questionary",
        )
        return QuestionaryResponse.parse_obj(response.json())

    async def patch(
        self, account_id: int, applicant_id: int, data: QuestionaryRequest,
    ) -> QuestionaryResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#patch-/accounts/-account_id-/applicants/-applicant_id-/questionary

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param data: Questionary data depends on the questionary schema.

        :return: Return updated questionary
        """
        response = await self._api.request(
            "PATCH",
            f"/accounts/{account_id}/applicants/{applicant_id}/questionary",
            json=data.jsonable_dict(exclude_none=True),
        )
        return QuestionaryResponse.parse_obj(response.json())
