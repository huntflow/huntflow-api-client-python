from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from huntflow_api_client.models.common import EditedFillQuota, FillQuota, JsonRequestModel
from huntflow_api_client.models.request.vacancies import VacancyCreateState, VacancyUpdateState

HTML_TAGS = "ul, ol, li, p, br, a, strong, em, u, b, i"


class VacancyBlock(BaseModel):
    fill_quotas: List[FillQuota] = Field(..., max_length=1, description="Fill quota ID")
    money: Optional[str] = Field(None, description="Salary")
    priority: Optional[int] = Field(
        None,
        description="The priority of a vacancy (0 for usual or 1 for high)",
        ge=0,
        le=1,
    )

    model_config = ConfigDict(extra="allow")


class MultiVacancyCreateRequest(JsonRequestModel):
    account_applicant_offer: Optional[PositiveInt] = Field(
        None,
        description="Organization offer ID",
    )
    position: str = Field(..., description="The name of the vacancy (occupation)")
    company: Optional[str] = Field(
        None,
        description="Department name (ignored if the divisions are enabled)",
    )
    hidden: bool = Field(False, description="Is the vacancy hidden from coworkers?")
    state: VacancyCreateState = Field(VacancyCreateState.OPEN, description="The state of a vacancy")
    coworkers: Optional[List[PositiveInt]] = Field(
        None,
        description="The list of coworker ID working with a vacancy",
    )
    body: Optional[str] = Field(
        None,
        description=(
            f"The responsibilities for a vacancy in HTML format. Available tags: {HTML_TAGS}"
        ),
    )
    requirements: Optional[str] = Field(
        None,
        description=f"The requirements for a vacancy in HTML format. Available tags: {HTML_TAGS}",
    )
    conditions: Optional[str] = Field(
        None,
        description=f"The conditions for a vacancy in HTML format. Available tags: {HTML_TAGS}",
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        description=("The list of file IDs to be attached to a vacancy (Upload files)"),
    )
    blocks: List[VacancyBlock] = Field(..., description="List of sub-vacancies for a multivacancy")

    model_config = ConfigDict(extra="allow")


class VacancyBlockUpdate(VacancyBlock):
    id: Optional[PositiveInt] = Field(None, description="Sub-vacancy ID")


class MultiVacancyUpdateRequest(JsonRequestModel):
    account_applicant_offer: Optional[PositiveInt] = Field(
        None,
        description="Organization offer ID",
    )
    position: str = Field(..., description="The name of the vacancy (occupation)")
    company: Optional[str] = Field(
        None,
        description="Department name (ignored if the divisions are enabled)",
    )
    hidden: bool = Field(False, description="Is the vacancy hidden from coworkers?")
    state: VacancyUpdateState = Field(VacancyUpdateState.OPEN, description="The state of a vacancy")
    body: Optional[str] = Field(
        None,
        description=(
            "The responsibilities for a vacancy in HTML format. Available tags: {html_tags}"
        ),
    )
    requirements: Optional[str] = Field(
        None,
        description=f"The requirements for a vacancy in HTML format. Available tags: {HTML_TAGS}",
    )
    conditions: Optional[str] = Field(
        None,
        description=f"The conditions for a vacancy in HTML format. Available tags: {HTML_TAGS}",
    )
    files: Optional[List[PositiveInt]] = Field(
        None,
        description="The list of file IDs to be attached to a vacancy (Upload files)",
    )
    blocks: List[VacancyBlockUpdate] = Field(
        ...,
        description="List of sub-vacancies for a multivacancy",
    )

    model_config = ConfigDict(extra="allow")


class VacancyBlockUpdatePartial(VacancyBlockUpdate):
    account_division: Optional[PositiveInt] = Field(
        None,
        description=(
            "Division ID. "
            "It cannot be null if the `use-divisions` setting is enabled in the organization."
        ),
    )
    fill_quotas: Optional[List[EditedFillQuota]] = Field(  # type: ignore
        None,
        max_length=1,
        description="Fill quota ID",
    )


class MultiVacancyPartialUpdateRequest(MultiVacancyUpdateRequest):
    blocks: List[VacancyBlockUpdatePartial] = Field(  # type: ignore
        ...,
        description="List of sub-vacancies for a multivacancy",
    )
