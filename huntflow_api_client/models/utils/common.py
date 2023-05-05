from enum import Enum


class WebhookEvent(str, Enum):
    APPLICANT = "APPLICANT"
    VACANCY = "VACANCY"
    RESPONSE = "RESPONSE"
    OFFER = "OFFER"
    VACANCY_REQUEST = "VACANCY-REQUEST"
