from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.response.applicant_on_vacancy_status import VacancyStatusesResponse


class ApplicantOnVacancyStatus(BaseEntity, ListEntityMixin):
    async def list(self, account_id: int) -> VacancyStatusesResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies/statuses

        :param account_id: Organization ID
        :return: List of available applicant on vacancy statuses (stages)
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/vacancies/statuses")
        return VacancyStatusesResponse.model_validate(response.json())
