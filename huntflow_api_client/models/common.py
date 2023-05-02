import json
from typing import Any, Dict

from pydantic import BaseModel


class JsonRequestModel(BaseModel):
    def jsonable_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        return json.loads(self.json(exclude_none=exclude_none))
