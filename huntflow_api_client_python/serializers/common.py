import typing as t
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class Applicant(BaseModel):
    first_name: t.Optional[str] = Field(None, description="First name", example="John")
    last_name: t.Optional[str] = Field(None, description="Last name", example="Doe")
    middle_name: str = Field(None, description="Middle name", example="Michael")
    money: str = Field(None, description="Salary expectation", example="$100000")
    phone: str = Field(None, description="Phone number", example="89999999999")
    email: EmailStr = Field(None, description="Email address", example="mail@mail.ru")
    skype: str = Field(None, description="Skype login", example="my_skype")
    position: str = Field(None, description="Applicant’s occupation", example="Front-end developer")
    company: str = Field(None, description="Applicant’s place of work", example="Google Inc.")
    photo: int = Field(None, description="Applicant’s photo ID", example=1)


class AgreementState(str, Enum):
    not_sent = "not_sent"
    sent = "sent"
    accepted = "accepted"
    declined = "declined"
