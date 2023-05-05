from pydantic import AnyHttpUrl, BaseModel, Field, PositiveInt


class File(BaseModel):
    id: PositiveInt = Field(..., description="File ID", example=19)
    url: AnyHttpUrl = Field(..., description="File URL")
    content_type: str = Field(..., description="MIME type of file", example="application/pdf")
    name: str = Field(..., description="File name", example="Resume.pdf")
