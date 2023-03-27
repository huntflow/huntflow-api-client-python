import json
from abc import ABC, abstractmethod

from .token import ApiToken


class AbstractHuntflowTokenStorage(ABC):
    @abstractmethod
    async def get(self) -> ApiToken:
        pass

    @abstractmethod
    async def update(self, token: ApiToken) -> None:
        pass


class HuntflowTokenFileStorage(AbstractHuntflowTokenStorage):
    def __init__(self, filename: str) -> None:
        self._filename = filename

    async def get(self) -> ApiToken:
        with open(self._filename) as fin:
            data = json.load(fin)
        return ApiToken.from_dict(data)

    async def update(self, token: ApiToken) -> None:
        with open(self._filename, "w") as fout:
            json.dump(token.dict(), fout, indent=4)
