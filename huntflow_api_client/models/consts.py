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
