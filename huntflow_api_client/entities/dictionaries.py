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
    DictionaryCreateResponse,
    DictionaryResponse,
    DictionaryUpdateResponse,
)


class Dictionary(BaseEntity, UpdateEntityMixin, ListEntityMixin, CreateEntityMixin, GetEntityMixin):
    async def list(self, account_id: int) -> DictionariesListResponse:  # noqa: A003 VNE003
        path = f"/accounts/{account_id}/dictionaries"
        response = await self._api.request("GET", path)
        data = DictionariesListResponse.parse_obj(response.json())
        return data

    async def create(
        self,
        account_id: int,
        data: DictionaryCreateRequest,
    ) -> DictionaryCreateResponse:
        path = f"/accounts/{account_id}/dictionaries"
        response = await self._api.request("POST", path, json=data.jsonable_dict(exclude_none=True))
        data = DictionaryCreateResponse.parse_obj(response.json())
        return data

    async def get(self, account_id: int, dict_code: str) -> DictionaryResponse:
        path = f"/accounts/{account_id}/dictionaries/{dict_code}"
        response = await self._api.request("GET", path)
        data = DictionaryResponse.parse_obj(response.json())
        return data

    async def update(
        self,
        account_id: int,
        dict_code: str,
        data: DictionaryUpdateRequest,
    ) -> DictionaryUpdateResponse:
        path = f"/accounts/{account_id}/dictionaries/{dict_code}"
        response = await self._api.request("PUT", path, json=data.jsonable_dict(exclude_none=True))

        data = DictionaryUpdateResponse.parse_obj(response.json())
        return data
