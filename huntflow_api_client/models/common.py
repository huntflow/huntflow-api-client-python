import json
from typing import Any, Dict

from pydantic import BaseModel


class JsonRequestModel(BaseModel):
    def jsonable_dict(self) -> Dict[str, Any]:
        return json.loads(self.json())
