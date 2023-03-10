import json
import time
from abc import ABC, abstractmethod
from dataclasses import asdict

from .huntflow_token import HuntflowApiToken


class AbstractHuntflowTokenStorage(ABC):
    @abstractmethod
    async def get(self) -> HuntflowApiToken:
        pass

    @abstractmethod
    async def update(self, token: HuntflowApiToken):
        pass


class HuntflowTokenFileStorage(AbstractHuntflowTokenStorage):
    def __init__(self, filename: str) -> None:
        self._filename = filename

    async def get(self) -> HuntflowApiToken:
        with open(self._filename) as fin:
            data = json.load(fin)
        return HuntflowApiToken.from_dict(data)

    async def update(self, token: HuntflowApiToken):
        with open(self._filename, "w") as fout:
            json.dump(asdict(token), fout, indent=4)
