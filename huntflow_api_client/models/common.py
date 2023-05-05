import json
from typing import AbstractSet, Any, Callable, Dict, Mapping, Optional, Union

from pydantic import BaseModel, Field, PositiveInt

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


class JsonRequestModel(BaseModel):
    def jsonable_dict(
        self,
        *,
        include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        **dumps_kwargs: Any,
    ) -> Dict[str, Any]:
        params = {
            "include": include,
            "exclude": exclude,
            "by_alias": by_alias,
            "skip_defaults": skip_defaults,
            "exclude_unset": exclude_unset,
            "exclude_defaults": exclude_defaults,
            "exclude_none": exclude_none,
            "encoder": encoder,
        }
        return json.loads(self.json(**params, **dumps_kwargs))  # type: ignore


class PaginatedResponse(BaseModel):
    page: PositiveInt = Field(..., description="Page number", example=1)
    count: int = Field(..., description="Number of items per page", example=30)
    total_pages: int = Field(..., description="Total number of pages", example=2)
