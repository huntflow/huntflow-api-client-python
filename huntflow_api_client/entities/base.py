import abc

from huntflow_api_client import HuntflowAPI


class BaseEntity:
    def __init__(self, api: HuntflowAPI):
        self._api: HuntflowAPI = api


class GetEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def get(self, *args, **kwargs):  # type: ignore
        pass


class ListEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def list(self, *args, **kwargs):  # type: ignore
        pass


class CreateEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def create(self, *args, **kwargs):  # type: ignore
        pass


class UpdateEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def update(self, *args, **kwargs):  # type: ignore
        pass


class DeleteEntityMixin(abc.ABC):
    @abc.abstractmethod
    async def delete(self, *args, **kwargs):  # type: ignore
        pass


class CRUDEntityMixin(
    GetEntityMixin,
    CreateEntityMixin,
    UpdateEntityMixin,
    DeleteEntityMixin,
):
    pass
