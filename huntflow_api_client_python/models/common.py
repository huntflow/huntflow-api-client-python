import json

from pydantic import BaseModel


class JsonRequestModel(BaseModel):
    def jsonable_dict(self) -> dict:
        return json.loads(self.json())
