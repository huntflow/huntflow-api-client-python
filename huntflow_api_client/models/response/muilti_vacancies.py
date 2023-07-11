from uuid import UUID

from pydantic import BaseModel, Field


class MultiVacancyResponse(BaseModel):
    job: UUID = Field(..., alias="task_id", description="Task ID")

    class Config:
        allow_population_by_field_name = True
