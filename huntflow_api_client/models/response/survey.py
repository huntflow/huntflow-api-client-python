from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SurveyTypesEnum(str, Enum):
    TYPE_A = "type_a"
    TYPE_Q = "type_q"


class BaseSurveySchemaType(BaseModel):
    id: int = Field(..., description="Survey ID")
    name: str = Field(..., description="Survey name")
    type: SurveyTypesEnum = Field(..., description="Survey type")
    active: bool = Field(..., description="Is survey active?")
    created: datetime = Field(..., description="Date and time of creating a survey")
    updated: datetime = Field(..., description="Date and time of the last update of the survey")


class SurveySchemaTypeQLogResponse(BaseSurveySchemaType):
    title: Optional[str] = Field(..., description="Survey title")
