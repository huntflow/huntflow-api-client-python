from enum import Enum


class WebhookEvent(str, Enum):
    APPLICANT = "APPLICANT"
    VACANCY = "VACANCY"
    RESPONSE = "RESPONSE"
    OFFER = "OFFER"
    VACANCY_REQUEST = "VACANCY-REQUEST"


class MemberType(str, Enum):
    owner = "owner"
    manager = "manager"
    watcher = "watcher"


class VacancyState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    HOLD = "HOLD"
    REOPEN = "REOPEN"
    VACANCY_REQUEST_ATTACH = "VACANCY_REQUEST_ATTACH"
    RESUME = "RESUME"
    CREATED = "CREATED"


class FieldType(str, Enum):
    string = "string"
    integer = "integer"
    text = "text"
    date = "date"
    select = "select"
    complex = "complex"
    contract = "contract"
    reason = "reason"
    stoplist = "stoplist"
    compensation = "compensation"
    dictionary = "dictionary"
    income = "income"
    position_status = "position_status"
    division = "division"
    region = "region"
    url = "url"
    hidden = "hidden"
    html = "html"


class AgreementState(str, Enum):
    not_sent = "not_sent"
    sent = "sent"
    accepted = "accepted"
    declined = "declined"


class CalendarEventType(str, Enum):
    interview = "interview"
    other = "other"


class Transparency(str, Enum):
    busy = "busy"
    free = "free"


class CalendarEventReminderMethod(str, Enum):
    popup = "popup"
    email = "email"


class EventReminderMultiplier(str, Enum):
    minutes = "minutes"
    hours = "hours"
    days = "days"
    weeks = "weeks"


class EmailContactType(str, Enum):
    cc = "cc"
    bcc = "bcc"
    to = "to"
