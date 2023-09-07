from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    GetEntityMixin,
    ListEntityMixin,
    UpdateEntityMixin,
)
from huntflow_api_client.models.request.dictionaries import (
    DictionaryCreateRequest,
    DictionaryUpdateRequest,
)
from huntflow_api_client.models.response.dictionaries import (
    DictionariesListResponse,
    DictionaryResponse,
    DictionaryTaskResponse,
)


class Dictionary(BaseEntity, UpdateEntityMixin, ListEntityMixin, CreateEntityMixin, GetEntityMixin):
    async def list(self, account_id: int) -> DictionariesListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/dictionaries

        :param account_id: Organization ID
        :return: List of organization's custom dictionaries
        """
        path = f"/accounts/{account_id}/dictionaries"
        response = await self._api.request("GET", path)
        data = DictionariesListResponse.model_validate(response.json())
        return data

    async def create(
        self,
        account_id: int,
        data: DictionaryCreateRequest,
    ) -> DictionaryTaskResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/dictionaries

        :param account_id: Organization ID
        :param data: Dictionary data
        :return: An object that contains the task ID of the delayed background update task
        """
        path = f"/accounts/{account_id}/dictionaries"
        response = await self._api.request("POST", path, json=data.jsonable_dict(exclude_none=True))
        return DictionaryTaskResponse.model_validate(response.json())

    async def get(self, account_id: int, dict_code: str) -> DictionaryResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/dictionaries/-dictionary_code-

        :param account_id: Organization ID
        :param dict_code: Dictionary code
        :return: The specified dictionary
        """
        path = f"/accounts/{account_id}/dictionaries/{dict_code}"
        response = await self._api.request("GET", path)
        return DictionaryResponse.model_validate(response.json())

    async def update(
        self,
        account_id: int,
        dict_code: str,
        data: DictionaryUpdateRequest,
    ) -> DictionaryTaskResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#put-/accounts/-account_id-/dictionaries/-dictionary_code-

        :param account_id: Organization ID
        :param dict_code: Dictionary code
        :param data: Dictionary data for update
        :return: An object that contains the task ID of the delayed background update task
        """
        path = f"/accounts/{account_id}/dictionaries/{dict_code}"
        response = await self._api.request("PUT", path, json=data.jsonable_dict(exclude_none=True))
        return DictionaryTaskResponse.model_validate(response.json())
