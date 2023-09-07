from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, Field, PositiveInt

from huntflow_api_client.models.common import File


class Name(BaseModel):
    first: Optional[str] = Field(None, description="Firstname")
    last: Optional[str] = Field(None, description="Lastname")
    middle: Optional[str] = Field(None, description="Middlename")


class Birthdate(BaseModel):
    year: Optional[PositiveInt] = Field(None, description="Year")
    month: Optional[PositiveInt] = Field(None, description="Month")
    day: Optional[PositiveInt] = Field(None, description="Day")
    precision: Optional[str] = Field(
        None,
        description="Precision of the date. Can be represented by values: "
        "year (2000) | month (2000-07) | day (2000-10-07)",
    )


class Experience(BaseModel):
    position: Optional[str] = Field(None, description="Position")
    company: Optional[str] = Field(None, description="Company name")


class ParsedFields(BaseModel):
    name: Optional[Name] = None
    birthdate: Optional[Birthdate] = None
    phones: Optional[List[str]] = Field(None, description="Phones")
    email: Optional[str] = Field(None, description="Email")
    salary: Optional[int] = Field(None, description="Salary")
    position: Optional[str] = Field(None, description="Position")
    skype: Optional[str] = Field(None, description="Skype")
    telegram: Optional[str] = Field(None, description="Telegram")
    experience: Optional[List[Experience]] = Field(None, description="Experience")


class UploadResponse(File):
    id: PositiveInt = Field(..., description="File ID")
    content_type: str = Field(..., description="File content type")
    name: str = Field(..., description="File name")
    url: AnyHttpUrl = Field(..., description="File URL")
    photo: Optional[File] = Field(None, description="Photo file")
    text: Optional[str] = Field(None, description="Parsed text")
    parsed_fields: Optional[ParsedFields] = Field(None, alias="fields", description="Parsed fields")
