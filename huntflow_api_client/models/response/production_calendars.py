from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, PositiveInt


class CalendarResponse(BaseModel):
    id: PositiveInt = Field(..., description="Calendar ID")  # noqa: VNE003, A003
    name: str = Field(..., description="Calendar name", example="Russian Federation")


class AccountCalendarResponse(BaseModel):
    account: PositiveInt = Field(..., description="Organization ID")
    production_calendar: PositiveInt = Field(..., description="Calendar ID")


class CalendarListResponse(BaseModel):
    items: List[CalendarResponse] = Field(
        ...,
        description="List of available production calendars",
    )


class NonWorkingDays(BaseModel):
    start: date = Field(..., description="Start date", example=date(2021, 2, 1))
    deadline: date = Field(..., description="Deadline date", example=date(2021, 2, 7))
    total_days: int = Field(..., description="Total amount of days within the range", example=7)
    not_working_days: int = Field(
        ...,
        description="Amount of non-working days within the range",
        example=2,
    )
    production_calendar: PositiveInt = Field(..., description="Calendar ID")


class NonWorkingDaysResponse(NonWorkingDays):
    items: Optional[List[date]] = Field(
        None,
        description="List of dates, weekends and holidays within the range",
        example=[date(2021, 2, 6), date(2021, 2, 7)],
    )


class NonWorkingDaysBulkResponse(BaseModel):
    items: List[NonWorkingDays] = Field(
        ...,
        description="Info about non-working days for several periods",
    )


class DatesBulkResponse(BaseModel):
    items: List[date] = Field(..., description="List of deadlines", example=[date(2020, 1, 1)])
