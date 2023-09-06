import datetime
from typing import Any, Dict, Optional

from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin, ListEntityMixin
from huntflow_api_client.models.request.production_calendars import (
    DeadLineDatesBulkRequest,
    NonWorkingDaysBulkRequest,
    StartDatesBulkRequest,
)
from huntflow_api_client.models.response.production_calendars import (
    AccountCalendarResponse,
    CalendarListResponse,
    CalendarResponse,
    DatesBulkResponse,
    NonWorkingDaysBulkResponse,
    NonWorkingDaysResponse,
)


class ProductionCalendar(BaseEntity, ListEntityMixin, GetEntityMixin):
    async def list(self) -> CalendarListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/production_calendars

        :return: List of production calendars
        """
        path = "/production_calendars"
        response = await self._api.request("GET", path)
        return CalendarListResponse.model_validate(response.json())

    async def get(self, calendar_id: int) -> CalendarResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/production_calendars/-calendar_id-

        :param calendar_id: Calendar ID
        :return: Information about the production calendar
        """
        path = f"/production_calendars/{calendar_id}"
        response = await self._api.request("GET", path)
        return CalendarResponse.model_validate(response.json())

    async def get_organizations_calendar(self, account_id: int) -> AccountCalendarResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/calendar

        :param account_id: Calendar ID
        :return: Organization's production calendar
        """
        path = f"/accounts/{account_id}/calendar"
        response = await self._api.request("GET", path)
        return AccountCalendarResponse.model_validate(response.json())

    async def get_non_working_days_in_period(
        self,
        calendar_id: int,
        deadline: datetime.date,
        start: Optional[datetime.date] = None,
        verbose: Optional[bool] = True,
    ) -> NonWorkingDaysResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/production_calendars/-calendar_id-/days/-deadline-

        :param calendar_id: Calendar ID
        :param deadline: Deadline date
        :param start: A date to start counting of non-working days
        :param verbose: Extends the response with the items field —
            list of dates, weekends and holidays within given range; in YYYY-MM-DD format
        :return: The total number of non-working/working days and
            a list of weekends and holidays within a range
        """
        params: Dict[str, Any] = {"verbose": verbose}
        if start:
            params["start"] = start.strftime("%Y-%m-%d")
        path = f"/production_calendars/{calendar_id}/days/{deadline}"
        response = await self._api.request("GET", path, params=params)
        return NonWorkingDaysResponse.model_validate(response.json())

    async def get_non_working_days_for_multiple_period(
        self,
        calendar_id: int,
        data: NonWorkingDaysBulkRequest,
    ) -> NonWorkingDaysBulkResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/production_calendars/-calendar_id-/days

        :param calendar_id: Calendar ID
        :param data: List of dictionaries with deadline, start fields
        :return: List of objects with the total number of non-working/working days for the
            specified periods
        """
        path = f"/production_calendars/{calendar_id}/days"
        response = await self._api.request("POST", path, content=data.model_dump_json())
        return NonWorkingDaysBulkResponse.model_validate(response.json())

    async def get_deadline_date_with_non_working_days(
        self,
        calendar_id: int,
        days: int,
        start: Optional[datetime.date] = None,
    ) -> str:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/production_calendars/-calendar_id-/deadline/-days-

        :param calendar_id: Calendar ID
        :param days: Working days amount
        :param start: A date to start counting
        :return: Deadline after {days} working days
        """
        params = None
        if start:
            params = {"start": start}
        path = f"/production_calendars/{calendar_id}/deadline/{days}"
        response = await self._api.request("GET", path, params=params)
        return response.json()

    async def get_multiple_deadline_dates_with_non_working_days(
        self,
        calendar_id: int,
        data: DeadLineDatesBulkRequest,
    ) -> DatesBulkResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/production_calendars/-calendar_id-/deadline

        :param calendar_id: Calendar ID
        :param data: List of dictionaries with days, start fields
        :return: List of deadlines
        """
        path = f"/production_calendars/{calendar_id}/deadline"
        response = await self._api.request("POST", path, content=data.model_dump_json())
        return DatesBulkResponse.model_validate(response.json())

    async def get_start_date_with_non_working_days(
        self,
        calendar_id: int,
        days: int,
        deadline: datetime.date,
    ) -> str:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/production_calendars/-calendar_id-/start/-days-

        :param calendar_id: Calendar ID
        :param days: Working days amount
        :param deadline: A date to start reverse counting
        :return: A date in {days} working days ahead, according to {calendar_id}
            production calendar
        """
        params = None
        if deadline:
            params = {"deadline": deadline}
        path = f"/production_calendars/{calendar_id}/start/{days}"
        response = await self._api.request("GET", path, params=params)
        return response.json()

    async def get_multiple_start_dates_with_non_working_days(
        self,
        calendar_id: int,
        data: StartDatesBulkRequest,
    ) -> DatesBulkResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#post-/production_calendars/-calendar_id-/start

        :param calendar_id: Calendar ID
        :param data: List of dictionaries with days, deadline fields
        :return: List of start dates
        """
        path = f"/production_calendars/{calendar_id}/start"
        response = await self._api.request("POST", path, content=data.model_dump_json())
        return DatesBulkResponse.model_validate(response.json())
