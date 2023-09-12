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
    send_error = "send_error"


class ApplicantSearchField(str, Enum):
    all = "all"
    education = "education"
    experience = "experience"
    position = "position"


class ApplicantLogType(str, Enum):
    ADD = "ADD"
    UPDATE = "UPDATE"
    VACANCY_ADD = "VACANCY-ADD"
    STATUS = "STATUS"
    COMMENT = "COMMENT"
    DOUBLE = "DOUBLE"
    AGREEMENT = "AGREEMENT"
    MAIL = "MAIL"
    RESPONSE = "RESPONSE"


class EmailContactType(str, Enum):
    cc = "cc"
    bcc = "bcc"
    to = "to"


class CalendarEventStatus(str, Enum):
    accepted = "accepted"
    declined = "declined"
    confirmed = "confirmed"
    tentative = "tentative"
    cancelled = "cancelled"
    needs_action = "needsAction"


class CalendarEventReminderMethod(str, Enum):
    popup = "popup"
    email = "email"


class CalendarEventType(str, Enum):
    interview = "interview"
    other = "other"


class Transparency(str, Enum):
    busy = "busy"
    free = "free"


class VacancyRequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class EventReminderMultiplier(str, Enum):
    minutes = "minutes"
    hours = "hours"
    days = "days"
    weeks = "weeks"


class TaskState(str, Enum):
    enqueued = "enqueued"
    inprogress = "inprogress"
    success = "success"
    failed = "failed"


class PrecisionTypes(str, Enum):
    year = "year"
    month = "month"
    day = "day"


class ActionLogType(str, Enum):
    SUCCESS_LOGIN = "SUCCESS_LOGIN"
    FAILED_LOGIN = "FAILED_LOGIN"
    LOGOUT = "LOGOUT"
    INVITE_ACCEPTED = "INVITE_ACCEPTED"
    NEW_AUTH_IN_ACCOUNT = "NEW_AUTH_IN_ACCOUNT"
    VACANCY_EXTERNAL = "VACANCY_EXTERNAL"
    ACCOUNT_MEMBER = "ACCOUNT_MEMBER"
    DOWNLOAD_APPLICANTS = "DOWNLOAD_APPLICANTS"


class SurveyType(str, Enum):
    TYPE_A = "type_a"
    TYPE_Q = "type_q"


class UserControlTaskAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class UserControlTaskStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
