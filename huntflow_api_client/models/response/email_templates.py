import typing as t

from pydantic import BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.common import EmailFollowup, File


class MailTemplateAttendee(BaseModel):
    type: str = Field(..., description="Attendee type")
    email: EmailStr = Field(..., description="Attendee email")


class MailTemplateDivision(BaseModel):
    id: PositiveInt = Field(..., description="Division ID")


class MailTemplate(BaseModel):
    id: PositiveInt = Field(..., description="Template ID")
    subject: t.Optional[str] = Field("", description="Subject text")
    name: str = Field(..., description="Template name")
    member: int = Field(..., description="Coworker ID who created the template")
    html: str = Field(..., description="HTML content")
    type: str = Field(..., description="Template type")
    followups: t.Optional[t.List[EmailFollowup]] = Field(None, description="Follow-up list")
    attendees: t.Optional[t.List[MailTemplateAttendee]] = Field(None, description="Attendees list")
    divisions: t.Optional[t.List[MailTemplateDivision]] = Field(None, description="Divisions list")
    files: t.Optional[t.List[File]] = Field(None, description="Files list")


class MailTemplatesResponse(BaseModel):
    items: t.List[MailTemplate]
