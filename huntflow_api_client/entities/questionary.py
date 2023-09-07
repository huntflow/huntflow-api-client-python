from typing import Any, Dict

from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    GetEntityMixin,
    UpdateEntityMixin,
)
from huntflow_api_client.models.response.questionary import QuestionarySchemaResponse


class ApplicantsQuestionary(BaseEntity, GetEntityMixin, CreateEntityMixin, UpdateEntityMixin):
    async def get_schema(self, account_id: int) -> QuestionarySchemaResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/questionary

        :param account_id: Organization ID

        :return: A schema of applicant's questionary for organization
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/applicants/questionary")
        return QuestionarySchemaResponse.model_validate(response.json())

    async def create(
        self,
        account_id: int,
        applicant_id: int,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        The successful response depends on the questionary schema

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
            json=data,
        )
        return response.json()

    async def get(self, account_id: int, applicant_id: int) -> Dict[str, Any]:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/applicants/-applicant_id-/questionary

        :param account_id: Organization ID
        :param applicant_id: Applicant ID

        :return: A questionary for the specified applicant
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/applicants/{applicant_id}/questionary",
        )
        return response.json()

    async def update(
        self,
        account_id: int,
        applicant_id: int,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        The successful response depends on the questionary schema

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
            json=data,
        )
        return response.json()
