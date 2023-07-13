from uuid import UUID

from pydantic import BaseModel, Field


class MultiVacancyResponse(BaseModel):
    task_id: UUID = Field(..., description="Task ID")
