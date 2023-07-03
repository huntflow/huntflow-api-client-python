from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, PositiveInt


class EmailAccount(BaseModel):
    id: PositiveInt = Field(..., description="Email account ID")
    name: str = Field(..., description="Email name")
    email: str = Field(..., description="Email address")
    receive: bool = Field(..., description="Is it possible to receive letters")
    send: bool = Field(..., description="Is it possible to send letters")
    last_sync: Optional[datetime] = Field(None, description="Date and time of last sync")


class EmailAccountsListResponse(BaseModel):
    items: List[EmailAccount] = Field(..., description="List of connected email accounts")


class Calendar(BaseModel):
    id: PositiveInt = Field(..., description="Calendar ID")
    foreign: Optional[str] = Field(None, description="Foreign value")
    name: str = Field(..., description="Calendar name")
    access_role: str = Field(..., description="Role")


class CalendarAccount(BaseModel):
    id: PositiveInt = Field(..., description="Calendar account ID")
    name: str = Field(..., description="Calendar account name")
    auth_type: str = Field(..., description="Authentication type")
    freebusy: bool = False
    calendars: List[Calendar] = Field(
        ...,
        description="List of calendars associated with the account",
    )


class CalendarAccountsListResponse(BaseModel):
    items: List[CalendarAccount] = Field(..., description="List of connected calendar accounts")
