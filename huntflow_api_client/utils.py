from enum import Enum
from typing import Any, Callable, Dict, Type, TypeVar

T = TypeVar("T", bound=Enum)


def extend_enum(inherited_enum: Type[T]) -> Callable:
    def wrapper(added_enum: Type[T]) -> Enum:
        joined: Dict[str, Any] = {}
        for item in inherited_enum:
            joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return Enum(added_enum.__name__, joined)

    return wrapper
