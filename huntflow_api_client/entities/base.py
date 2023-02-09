import abc

import httpx

from huntflow_api_client import HuntflowAPI


class BaseEntity:
    def __init__(self, api: HuntflowAPI):
        self._client: httpx.AsyncClient = api.http_client


class GetEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def get(self, *args, **kwargs):
        pass


class ListEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def list(self, *args, **kwargs):
        pass


class CreateEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def create(self, *args, **kwargs):
        pass


class UpdateEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def update(self, *args, **kwargs):
        pass


class DeleteEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def delete(self, *args, **kwargs):
        pass


class CRUDEntityMixin(
    abc.ABC,
    GetEntityMixin,
    CreateEntityMixin,
    UpdateEntityMixin,
    DeleteEntityMixin,
):
    pass
