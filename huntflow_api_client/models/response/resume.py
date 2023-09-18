import typing as t
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from huntflow_api_client.models.common import File
from huntflow_api_client.models.consts import PrecisionTypes
from huntflow_api_client.models.response.applicants import ApplicantResume


class Portfolio(BaseModel):
    small: t.Optional[str] = Field(None, description="Small image url")
    large: t.Optional[str] = Field(None, description="Large image url")
    description: t.Optional[str] = Field(None, description="Image description")


class PhotoData(BaseModel):
    small: t.Optional[str] = Field(None, description="Small image url")
    medium: t.Optional[str] = Field(None, description="Medium image url")
    large: t.Optional[str] = Field(None, description="Large image url")
    external_id: t.Optional[str] = Field(None, description="Photo external ID")
    description: t.Optional[str] = Field(None, description="Photo description")
    source: t.Optional[str] = Field(None, description="Photo's source url")
    id: t.Optional[int] = Field(None, description="Huntflow photo ID")


class DateWithPrecision(BaseModel):
    year: t.Optional[int] = Field(None, description="Year")
    month: t.Optional[int] = Field(None, description="Month")
    day: t.Optional[int] = Field(None, description="Day")
    precision: PrecisionTypes = Field(..., description="Precision type")


class TextBlock(BaseModel):
    header: t.Optional[str] = Field(None, description="Text block header")
    body: t.Optional[str] = Field(None, description="Text block body")


class PersonalInfo(BaseModel):
    photo: t.Optional[PhotoData] = Field(None, description="Urls for resume photo")
    first_name: t.Optional[str] = Field(None, description="First name")
    middle_name: t.Optional[str] = Field(None, description="Middle name")
    last_name: t.Optional[str] = Field(None, description="Last name")
    birth_date: t.Optional[DateWithPrecision] = Field(None, description="Date of birth")
    text_block: t.Optional[TextBlock] = Field(None, description='Additional "About" info')


class ExternalEntity(BaseModel):
    id: t.Optional[t.Union[int, str]] = Field(None, description="Entity ID in Huntflow system")
    external_id: t.Optional[str] = Field(None, description="Entity external ID")
    name: t.Optional[str] = Field(None, description="Entity name")


class Area(BaseModel):
    country: t.Optional[ExternalEntity] = Field(None, description="Country")
    city: t.Optional[ExternalEntity] = Field(None, description="City")
    metro: t.Optional[ExternalEntity] = Field(None, description="Metro station")
    address: t.Optional[str] = Field(None, description="Full address")
    lat: t.Optional[float] = Field(None, description="Latitude")
    lng: t.Optional[float] = Field(None, description="Longitude")


class Specialization(ExternalEntity):
    profarea_id: t.Optional[str] = Field(None, description="Specialization ID in Huntflow system")
    external_profarea_id: t.Optional[str] = Field(None, description="Specialization external ID")
    prefarea_name: t.Optional[str] = Field(None, description="Specialization name")


class Skill(BaseModel):
    title: str = Field(..., description="Skill name")


class BaseEducationInfo(BaseModel):
    name: t.Optional[str] = Field(None, description="Education name")
    description: t.Optional[str] = Field(None, description="Education description")
    date_from: t.Optional[DateWithPrecision] = Field(None, description="Education start date")
    date_to: t.Optional[DateWithPrecision] = Field(None, description="Education end date")
    area: t.Optional[Area] = Field(None, description="Education area")


class EducationInfoWithResult(BaseEducationInfo):
    result: t.Optional[str] = Field(None, description="Education result")


class ExtendedEducationInfo(BaseEducationInfo):
    faculty: t.Optional[str] = Field(None, description="Faculty name")
    form: t.Optional[ExternalEntity]


class Experience(BaseModel):
    position: t.Optional[str] = Field(None, description="Position")
    date_from: t.Optional[DateWithPrecision] = Field(None, description="Experience start date")
    date_to: t.Optional[DateWithPrecision] = Field(None, description="Experience end date")
    company: t.Optional[str] = Field(None, description="Company name")
    url: t.Optional[str] = Field(None, description="Company's url")
    area: t.Optional[Area] = Field(None, description="Experience area")
    industries: t.Optional[t.List[ExternalEntity]] = Field(
        None,
        description="List of experience industries",
    )
    description: t.Optional[str] = Field(None, description="Experience description")
    skills: t.Optional[t.List[Skill]] = Field(None, description="List of skills")


class Attestation(BaseModel):
    date: t.Optional[DateWithPrecision]
    name: t.Optional[str]
    organization: t.Optional[str]
    description: t.Optional[str]
    result: t.Optional[str]


class Education(BaseModel):
    level: t.Optional[ExternalEntity] = Field(None, description="Education level")
    higher: t.Optional[t.List[ExtendedEducationInfo]] = Field(
        None,
        description="List of higher education institutions",
    )
    vocational: t.Optional[t.List[ExtendedEducationInfo]] = Field(
        None,
        description="List of vocational education institutions",
    )
    elementary: t.Optional[t.List[BaseEducationInfo]] = Field(
        None,
        description="List of elementary education institutions",
    )
    additional: t.Optional[t.List[EducationInfoWithResult]] = Field(
        None,
        description="List of additional education institutions",
    )
    attestation: t.Optional[t.List[Attestation]] = Field(None, description="List of attestations")


class Certificate(BaseModel):
    name: t.Optional[str] = Field(None, description="Name of certificate")
    organization: t.Optional[str] = Field(
        None,
        description="The organization that issued the certificate",
    )
    description: t.Optional[str] = Field(None, description="Certificate description")
    url: t.Optional[str] = Field(None, description="Certificate url")
    area: t.Optional[Area] = Field(None, description="Area of issue of the certificate")
    date: t.Optional[DateWithPrecision] = Field(
        None,
        description="Date of issue of the certificate",
    )


class ContactFullValue(BaseModel):
    country: str = Field()
    city: str = Field()
    number: str = Field()
    formatted: str = Field()


class Contact(BaseModel):
    type: t.Optional[ExternalEntity] = Field(None, description="Contact type")
    value: t.Optional[str] = Field(None, description="Contact value")
    preferred: t.Optional[bool] = Field(
        None,
        description="This is the preferred method of communication",
    )
    full_value: t.Optional[ContactFullValue] = Field(
        None,
        description="If contact is a phone number - additional data about it",
    )


class Relocation(BaseModel):
    type: t.Optional[ExternalEntity] = Field(None, description="Type of relocation")
    area: t.Optional[t.List[Area]] = Field(None, description="List of areas for relocation")


class Language(ExternalEntity):
    level: t.Optional[ExternalEntity] = Field(None, description="Language proficiency level")


class Salary(BaseModel):
    amount: t.Optional[float] = Field(None, description="Salary amount")
    currency: t.Optional[str] = Field(None, description="Salary currency")


class Recommendation(BaseModel):
    value: t.Optional[str] = Field(None, description="Recommendation")
    date: t.Optional[DateWithPrecision] = Field(None, description="Date of recommendation")
    name: t.Optional[str] = Field(None, description="Name to whom recommendation")
    position: t.Optional[str] = Field(None, description="Position")
    organization: t.Optional[str] = Field(None, description="Organization name")
    contact: t.Optional[str] = Field(None, description="Contact")


class SimplePhoto(BaseModel):
    url: t.Optional[str] = Field(None, description="Photo url")
    original: t.Optional[str] = Field(None, description="Photo original")


class Additional(BaseModel):
    name: t.Optional[str] = Field(None, description="Name of additional info")
    description: t.Optional[str] = Field(None, description="Description of additional info")


class Military(BaseModel):
    date_from: t.Optional[DateWithPrecision] = Field(
        None,
        description="Military service start date",
    )
    date_to: t.Optional[DateWithPrecision] = Field(None, description="Military service end date")
    area: t.Optional[Area] = Field(None, description="Military service area")
    unit: t.Optional[dict] = Field(
        None,
        description="Military service unit",
    )


class SocialRating(BaseModel):
    kind: t.Optional[str]
    stats: t.Optional[t.Any]
    tags: t.Optional[t.List[str]]
    url: t.Optional[str]
    login: t.Optional[str]
    registered_at: t.Optional[str] = Field(None, description="ISO datetime")


class Resume(BaseModel):
    personal_info: t.Optional[PersonalInfo] = Field(None, description="Personal info")
    source_url: t.Optional[str] = Field(None, description="Resume url to external job site")
    position: t.Optional[str] = Field(None, description="Resume header")
    specialization: t.Optional[t.List[Specialization]] = Field(None, description="Specializations")
    skill_set: t.Optional[t.List[str]] = Field(None, description="List of skills")
    gender: t.Optional[ExternalEntity] = Field(None, description="Gender")
    experience: t.Optional[t.List[Experience]] = Field(None, description="Work experiences")
    education: t.Optional[Education] = Field(None, description="Education")
    certificate: t.Optional[t.List[Certificate]] = Field(None, description="Certificates")
    portfolio: t.Optional[t.List[PhotoData]] = Field(None, description="Portfolio")
    contact: t.Optional[t.List[Contact]] = Field(None, description="List of contacts")
    area: t.Optional[Area] = Field(None, description="Living area")
    relocation: t.Optional[Relocation] = Field(None, description="Relocation info")
    citizenship: t.Optional[t.List[ExternalEntity]] = Field(None, description="Citizenship")
    work_permit: t.Optional[t.List[ExternalEntity]] = Field(
        None,
        description="List of countries with work permission",
    )
    language: t.Optional[t.List[Language]] = Field(None, description="Language proficiency")
    wanted_salary: t.Optional[Salary] = Field(None, description="Desired salary")
    work_schedule: t.Optional[t.List[ExternalEntity]] = Field(None, description="Work schedules")
    business_trip_readiness: t.Optional[ExternalEntity] = Field(
        None,
        description="Readiness for business trips",
    )
    recommendations: t.Optional[t.List[Recommendation]] = Field(
        None,
        description="List of recommendations",
    )
    has_vehicle: t.Optional[bool] = Field(None, description="Ownership of vehicle")
    driver_license_types: t.Optional[t.List[str]] = Field(
        None,
        description="List of available driver's licenses",
    )
    military: t.Optional[t.List[Military]] = Field(None, description="Military service")
    social_ratings: t.Optional[t.List[SocialRating]] = Field(None, description="Social ratings")
    photos: t.Optional[t.List[SimplePhoto]] = Field(None, description="Photos")
    additionals: t.Optional[t.List[Additional]] = Field(
        None,
        description="Some additional info related to resume",
    )
    wanted_place_of_work: t.Optional[str] = Field(None, description="Desired place of work")
    updated_on_source: t.Optional[DateWithPrecision] = Field(
        None,
        description="Date of resume update in the source",
    )
    travel_time: t.Optional[ExternalEntity] = Field(None, description="Preferred travel time")


class RawData(BaseModel):
    body: t.Optional[str] = Field(
        None,
        description="Resume text (for resumes with auth_type = NATIVE)",
    )

    model_config = ConfigDict(extra="allow")


class ApplicantResumeResponse(ApplicantResume):
    created: datetime = Field(..., description="The date and time of resume create")
    files: t.Optional[t.List[File]] = Field(None, description="List of files")
    source_url: t.Optional[str] = Field(None, description="Link to resume source")
    foreign: str = Field(..., description="Foreign resume ID")
    key: t.Optional[str] = Field(None, description="Resume key")
    portfolio: t.Optional[t.List[Portfolio]] = Field(None, description="Portfolio images")
    data: t.Optional[RawData] = Field(
        None,
        description="Raw resume data (format depends on auth_type)",
    )
    resume: t.Optional[Resume] = Field(None, description="Resume data in unified format")


class ApplicantSource(BaseModel):
    id: int = Field(..., description="Applicant source ID")
    foreign: t.Optional[str] = Field(None, description="Applicant source foreign")
    name: str = Field(..., description="Applicant source name")
    type: str = Field(..., description="Applicant source type")


class ApplicantSourcesResponse(BaseModel):
    items: t.List[ApplicantSource] = Field(..., description="List of applicant's sources")
