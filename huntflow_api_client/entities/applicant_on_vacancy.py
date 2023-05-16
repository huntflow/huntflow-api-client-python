from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.request.applicant_on_vacancy import (
    AddApplicantToVacancyRequest,
    ApplicantVacancySplitRequest,
    ChangeVacancyApplicantStatusRequest,
)
from huntflow_api_client.models.response.applicant_on_vacancy import (
    AddApplicantToVacancyResponse,
    ApplicantVacancySplitResponse,
    RejectionReasonsListResponse,
    VacancyStatusesResponse,
)


class ApplicantOnVacancy(BaseEntity, ListEntityMixin):
    async def list(self, account_id: int) -> VacancyStatusesResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/vacancies/statuses

        :param account_id: Organization ID
        :return: List of available applicant on vacancy statuses (stages)
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/vacancies/statuses")
        return VacancyStatusesResponse.parse_obj(response.json())

    async def rejection_reasons_list(self, account_id: int) -> RejectionReasonsListResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/rejection_reasons

        :param account_id: Organization ID
        :return: List of applicant on vacancy rejection reasons
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/rejection_reasons")
        return RejectionReasonsListResponse.parse_obj(response.json())

    async def attach_applicant_to_vacancy(
        self,
        account_id: int,
        applicant_id: int,
        data: AddApplicantToVacancyRequest,
    ) -> AddApplicantToVacancyResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/applicants/-applicant_id-/vacancy

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param data: Data for attaching the applicant to the vacancy
        :return: Info about attaching.
        """
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/applicants/{applicant_id}/vacancy",
            json=data.jsonable_dict(exclude_none=True),
        )
        return AddApplicantToVacancyResponse.parse_obj(response.json())

    async def update_vacancy_status_for_applicant(
        self,
        account_id: int,
        applicant_id: int,
        data: ChangeVacancyApplicantStatusRequest,
    ) -> AddApplicantToVacancyResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/applicants/-applicant_id-/vacancy

        :param account_id: Organization ID
        :param applicant_id: Applicant ID
        :param data: Data for changing the vacancy status for an applicant
        :return: Info about updating.
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/applicants/{applicant_id}/vacancy",
            json=data.jsonable_dict(exclude_none=True),
        )
        return AddApplicantToVacancyResponse.parse_obj(response.json())

    async def move_applicant_to_child_vacancy(
        self,
        account_id: int,
        vacancy_id: int,
        data: ApplicantVacancySplitRequest,
    ) -> ApplicantVacancySplitResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/applicants/vacancy/-vacancy_id-/split

        :param account_id: Organization ID
        :param vacancy_id: Vacancy ID
        :param data: Data for moving an applicant to child vacancy
        :return: Info about moving.
        """
        response = await self._api.request(
            "PUT",
            f"/accounts/{account_id}/applicants/vacancy/{vacancy_id}/split",
            json=data.jsonable_dict(exclude_none=True),
        )
        return ApplicantVacancySplitResponse.parse_obj(response.json())