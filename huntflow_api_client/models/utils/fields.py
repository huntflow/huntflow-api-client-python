from datetime import datetime
from typing import Generator, Union

from pydantic import datetime_parse
from pydantic.datetime_parse import StrBytesIntFloat


class DatetimeWithTZ(datetime):
    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[datetime, StrBytesIntFloat]) -> datetime:
        if not isinstance(value, datetime):
            value = datetime_parse.parse_datetime(value)
        return value

    def __repr__(self) -> str:
        return f"DatetimeWIthTZ({super().__repr__()})"
