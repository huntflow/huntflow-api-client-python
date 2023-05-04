import typing as t

from pydantic import BaseModel, Field, PositiveInt


class ListResponseMixin(BaseModel):
    page: PositiveInt = Field(..., description="Page number", example=1)
    count: int = Field(..., description="Number of items per page", example=30)
    total_pages: int = Field(..., description="Total number of pages", example=2)
    total_items: t.Optional[int] = Field(None, description="Total number of items", example=50)

    class Config:
        allow_population_by_field_name = True

    def dict(self, *args, **kwargs) -> t.Dict[str, t.Any]:  # type: ignore # noqa A003
        exclude = kwargs.get("exclude")

        # if backend does not returns total_items parameter - remove it from response object
        if self.total_items is None:
            if exclude and isinstance(exclude, dict):
                exclude["total_items"] = ...
            elif exclude and isinstance(exclude, set):
                exclude.add("total_items")
            elif not exclude:
                exclude = {"total_items"}

        kwargs["exclude"] = exclude

        return super().dict(*args, **kwargs)
