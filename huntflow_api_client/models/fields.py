from enum import Enum

from pydantic import AnyHttpUrl, BaseModel, Field, PositiveInt


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


class File(BaseModel):
    id: PositiveInt = Field(..., description="File ID", example=19)
    url: AnyHttpUrl = Field(..., description="File URL")
    content_type: str = Field(..., description="MIME type of file", example="application/pdf")
    name: str = Field(..., description="File name", example="Resume.pdf")
