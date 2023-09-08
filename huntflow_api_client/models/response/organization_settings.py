from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from huntflow_api_client.models.consts import SurveyType


class HoldReason(BaseModel):
    id: Optional[int] = Field(None, description="Reason ID")
    name: str = Field(..., description="Reason name")


class HoldReasonsListResponse(BaseModel):
    items: List[HoldReason]


class CloseReason(BaseModel):
    id: Optional[int] = Field(None, description="Reason ID")
    name: str = Field(..., description="Reason name")


class CloseReasonsListResponse(BaseModel):
    items: List[CloseReason]


class BaseSurveySchemaType(BaseModel):
    id: int = Field(..., description="Survey ID")
    name: str = Field(..., description="Survey name")
    type: SurveyType = Field(..., description="Type of survey")
    active: bool = Field(..., description="Is survey active?")
    created: datetime = Field(..., description="Date and time of creating a survey")
    updated: datetime = Field(..., description="Date and time of the last update of the survey")


class BaseSurveySchemaTypeWithSchemas(BaseSurveySchemaType):
    json_schema: dict = Field(..., alias="schema", description="JSON schema for the survey fields")
    ui_schema: dict = Field(..., description="UI schema for the survey fields")
