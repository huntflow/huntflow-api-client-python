import typing as t

from pydantic import BaseModel, Field, AnyHttpUrl, PositiveInt


class OrganizationInfoResponse(BaseModel):
    id: PositiveInt = Field(..., description="Organization ID", example=10)
    name: str = Field(..., description="Organization name", example="Huntflow")
    nick: str = Field(..., description="Short organization name", example="huntflow")
    locale: str = Field(..., description="Organization locale", example="ru_RU")
    photo: t.Optional[AnyHttpUrl] = Field(
        None, description="Organization logo url", example="https://huntflow.ru/logo.jpg",
    )
