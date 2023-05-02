from datetime import datetime

from pydantic import datetime_parse


class DatetimeWithTZ(datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(example="2020-01-01T00:00:00+03:00")

    @classmethod
    def validate(cls, value):
        if not isinstance(value, datetime):
            value: datetime = datetime_parse.parse_datetime(value)

        return value

    def __repr__(self):
        return f"DatetimeWIthTZ({super().__repr__()})"
