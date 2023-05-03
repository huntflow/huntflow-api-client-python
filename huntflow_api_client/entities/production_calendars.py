import datetime

from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin, ListEntityMixin
from huntflow_api_client.models.request.production_calendars import (
    DeadLineDatesBulkRequest,
    NonWorkingDaysBulkRequest,
    StartDatesBulkRequest,
)
from huntflow_api_client.models.response.production_calendars import (
    AccountCalendar,
    CalendarListResponse,
    CalendarResponse,
    DatesBulkResponse,
    NonWorkingDaysBulkResponse,
    NonWorkingDaysResponse,
)

TODAY = datetime.date.today().strftime("%Y-%m-%d")


class ProductionCalendar(BaseEntity, ListEntityMixin, GetEntityMixin):
    async def list(self) -> CalendarListResponse:  # noqa: A003
        """
        Returns a list of production calendars
        """
        path = "/production_calendars"
        response = await self._api.request("GET", path)
        return CalendarListResponse.parse_obj(response.json())

    async def get(self, calendar_id: int) -> CalendarResponse:
        """
        Returns a production calendar by id
        """
        path = f"/production_calendars/{calendar_id}"
        response = await self._api.request("GET", path)
        return CalendarResponse.parse_obj(response.json())

    async def get_organizations_calendar(self, account_id: int) -> AccountCalendar:
        """
        Get organization's production calendar by organization id
        """
        path = f"/accounts/{account_id}/calendar"
        response = await self._api.request("GET", path)
        return AccountCalendar.parse_obj(response.json())

    async def get_non_working_days_in_period(
        self,
        calendar_id: int,
        deadline: str,
        start: str = TODAY,
        verbose: bool = True,
    ) -> NonWorkingDaysResponse:
        """
        Returns the total number of non-working/working days
        and a list of weekends and holidays within a range
        """
        params = {"start": start, "verbose": verbose}
        path = f"/production_calendars/{calendar_id}/days/{deadline}"
        response = await self._api.request("GET", path, params=params)
        return NonWorkingDaysResponse.parse_obj(response.json())

    async def get_non_working_days_for_multiple_period(
        self,
        calendar_id: int,
        data: NonWorkingDaysBulkRequest,
    ) -> NonWorkingDaysBulkResponse:
        """
        Returns a list of objects with the total number of non-working/working days
        for the specified periods. Objects do not contain verbose information,
        as if you were making a single request
        """
        path = f"/production_calendars/{calendar_id}/days"
        response = await self._api.request("POST", path, data=data.json())
        return NonWorkingDaysBulkResponse.parse_obj(response.json())

    async def get_deadline_date_with_non_working_days(
        self,
        calendar_id: int,
        days: int,
        start: str,
    ) -> str:
        """
        Returns a deadline after {days} working days
        """
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
        Returns a list of deadlines
        """
        path = f"/production_calendars/{calendar_id}/deadline"
        response = await self._api.request("POST", path, data=data.json())
        return DatesBulkResponse.parse_obj(response.json())

    async def get_start_date_with_non_working_days(
        self,
        calendar_id: int,
        days: int,
        deadline: str,
    ) -> str:
        """
        Returns a date in {days} working days ahead, according to {calendar_id} production calendar.
        """
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
        Returns a list of start dates
        """
        path = f"/production_calendars/{calendar_id}/start"
        response = await self._api.request("POST", path, data=data.json())
        return DatesBulkResponse.parse_obj(response.json())
