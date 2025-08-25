from enum import Enum
from typing import Callable, Type


def extend_enum(inherited_enum: Type[Enum]) -> Callable:
    def wrapper(added_enum: Type[Enum]) -> Enum:
        joined = {}
        for item in inherited_enum:
            joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return Enum(added_enum.__name__, joined)

    return wrapper
