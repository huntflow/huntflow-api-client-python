from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel


class NonWorkingDays(BaseModel):
    deadline: date = Field(..., description="Deadline date")
    start: Optional[date] = Field(None, description="Start date")


class NonWorkingDaysBulkRequest(RootModel):
    root: List[NonWorkingDays]


class DeadLineDate(BaseModel):
    days: int = Field(..., description="Amount of working days")
    start: Optional[date] = Field(None, description="A date to start counting. Default is today")


class DeadLineDatesBulkRequest(RootModel):
    root: List[DeadLineDate]


class StartDate(BaseModel):
    days: int = Field(..., description="Amount of working days")
    deadline: Optional[date] = Field(
        None,
        description="A date to finish the reverse counting. Default is today.",
    )


class StartDatesBulkRequest(RootModel):
    root: List[StartDate]
