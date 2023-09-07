import datetime

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.production_calendars import ProductionCalendar
from huntflow_api_client.models.request.production_calendars import (
    DeadLineDate,
    DeadLineDatesBulkRequest,
    NonWorkingDays,
    NonWorkingDaysBulkRequest,
    StartDate,
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
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
CALENDAR_ID = 1
TODAY = datetime.date.today()
DEADLINE_DATE = datetime.date(2023, 1, 1)
START_DATE = datetime.date(2023, 4, 1)
DAYS_COUNT = 2
CALENDAR_LIST_RESPONSE = {
    "items": [{"id": 1, "name": "Russian Federation"}, {"id": 2, "name": "Kazakhstan"}],
}
CALENDAR_GET_RESPONSE = {"id": 1, "name": "Russian Federation"}
ORG_CALENDAR_GET_RESPONSE = {"account": 19, "production_calendar": 1}
NON_WORKING_DAYS_GET_RESPONSE = {
    "start": TODAY.strftime("%Y-%m-%d"),
    "deadline": DEADLINE_DATE.strftime("%Y-%m-%d"),
    "total_days": 5,
    "not_working_days": 1,
    "production_calendar": 1,
    "items": [],
}
MULTIPLE_NON_WORKING_DAYS_GET_RESPONSE = {
    "items": [
        {
            "start": TODAY.strftime("%Y-%m-%d"),
            "deadline": DEADLINE_DATE.strftime("%Y-%m-%d"),
            "total_days": 7,
            "not_working_days": 2,
            "production_calendar": 1,
        },
    ],
}
DEADLINE_RESPONSE = "2023-04-03"
MULTIPLE_DEADLINE_RESPONSE = {"items": ["2020-01-01", "2021-12-12"]}
START_RESPONSE = "2020-06-08"
MULTIPLE_START_RESPONSE = {"items": ["1999-08-01", "1997-07-12"]}


async def test_list_calendar(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/production_calendars",
        json=CALENDAR_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    response = await calendars.list()
    assert response == CalendarListResponse.model_validate(CALENDAR_LIST_RESPONSE)


async def test_get_calendar(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/production_calendars/{CALENDAR_ID}",
        json=CALENDAR_GET_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    response = await calendars.get(calendar_id=1)
    assert response == CalendarResponse.model_validate(CALENDAR_GET_RESPONSE)


async def test_get_organizations_calendar(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/calendar",
        json=ORG_CALENDAR_GET_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    response = await calendars.get_organizations_calendar(account_id=ACCOUNT_ID)
    assert response == AccountCalendarResponse.model_validate(ORG_CALENDAR_GET_RESPONSE)


async def test_get_non_working_days_in_period(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/production_calendars/{CALENDAR_ID}/days/"
        f"{DEADLINE_DATE.strftime('%Y-%m-%d')}?verbose=true",
        json=NON_WORKING_DAYS_GET_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    response = await calendars.get_non_working_days_in_period(calendar_id=1, deadline=DEADLINE_DATE)
    assert response == NonWorkingDaysResponse.model_validate(NON_WORKING_DAYS_GET_RESPONSE)


async def test_get_non_working_days_for_multiple_period(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/production_calendars/{CALENDAR_ID}/days",
        json=MULTIPLE_NON_WORKING_DAYS_GET_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    data = NonWorkingDaysBulkRequest(
        root=[
            NonWorkingDays(deadline=datetime.date(2022, 10, 10), start=datetime.date(2021, 10, 10)),
            NonWorkingDays(deadline=datetime.date(2023, 10, 10), start=datetime.date(2022, 10, 10)),
        ],
    )
    response = await calendars.get_non_working_days_for_multiple_period(calendar_id=1, data=data)
    assert response == NonWorkingDaysBulkResponse.model_validate(
        MULTIPLE_NON_WORKING_DAYS_GET_RESPONSE,
    )


async def test_get_deadline_date_with_non_working_days(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/production_calendars/{CALENDAR_ID}/deadline/{DAYS_COUNT}?start="
        f"{START_DATE}",
        json=DEADLINE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    response = await calendars.get_deadline_date_with_non_working_days(
        calendar_id=1,
        days=DAYS_COUNT,
        start=START_DATE,
    )
    assert response == DEADLINE_RESPONSE


async def test_get_multiple_deadline_dates_with_non_working_days(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/production_calendars/{CALENDAR_ID}/deadline",
        json=MULTIPLE_DEADLINE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    data = DeadLineDatesBulkRequest(
        root=[
            DeadLineDate(days=100, start=datetime.date(2021, 10, 10)),
            DeadLineDate(days=5, start=datetime.date(2022, 10, 10)),
        ],
    )

    response = await calendars.get_multiple_deadline_dates_with_non_working_days(
        calendar_id=1,
        data=data,
    )
    assert response == DatesBulkResponse.model_validate(MULTIPLE_DEADLINE_RESPONSE)


async def test_get_start_date_with_non_working_days(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/production_calendars/{CALENDAR_ID}/start/{DAYS_COUNT}?deadline="
        f"{DEADLINE_DATE}",
        json=DEADLINE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    response = await calendars.get_start_date_with_non_working_days(
        calendar_id=1,
        days=DAYS_COUNT,
        deadline=DEADLINE_DATE,
    )
    assert response == DEADLINE_RESPONSE


async def test_get_multiple_start_dates_with_non_working_days(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/production_calendars/{CALENDAR_ID}/start",
        json=MULTIPLE_START_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    calendars = ProductionCalendar(api_client)

    data = StartDatesBulkRequest(
        root=[
            StartDate(days=100, deadline=datetime.date(2021, 10, 10)),
            StartDate(days=200, deadline=datetime.date(2019, 7, 17)),
        ],
    )

    response = await calendars.get_multiple_start_dates_with_non_working_days(
        calendar_id=1,
        data=data,
    )
    assert response == DatesBulkResponse.model_validate(MULTIPLE_START_RESPONSE)
