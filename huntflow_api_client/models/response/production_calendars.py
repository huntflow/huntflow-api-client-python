from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, PositiveInt


class CalendarResponse(BaseModel):
    id: PositiveInt = Field(..., description="Calendar ID")
    name: str = Field(..., description="Calendar name")


class AccountCalendarResponse(BaseModel):
    account: PositiveInt = Field(..., description="Organization ID")
    production_calendar: PositiveInt = Field(..., description="Calendar ID")


class CalendarListResponse(BaseModel):
    items: List[CalendarResponse] = Field(
        ...,
        description="List of available production calendars",
    )


class NonWorkingDays(BaseModel):
    start: date = Field(..., description="Start date")
    deadline: date = Field(..., description="Deadline date")
    total_days: int = Field(..., description="Total amount of days within the range")
    not_working_days: int = Field(
        ...,
        description="Amount of non-working days within the range",
    )
    production_calendar: PositiveInt = Field(..., description="Calendar ID")


class NonWorkingDaysResponse(NonWorkingDays):
    items: Optional[List[date]] = Field(
        None,
        description="List of dates, weekends and holidays within the range",
    )


class NonWorkingDaysBulkResponse(BaseModel):
    items: List[NonWorkingDays] = Field(
        ...,
        description="Info about non-working days for several periods",
    )


class DatesBulkResponse(BaseModel):
    items: List[date] = Field(..., description="List of deadlines")
