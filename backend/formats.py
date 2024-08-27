from enum import Enum
from typing import List

from pydantic import BaseModel, Field, conlist


class SectionNames(str, Enum):
    SECTION1 = "Introduction"
    SECTION2 = "Data Controller Information"
    SECTION3 = "Data Collection and Usage"
    SECTION4 = "Data Subject Rights"
    SECTION5 = "Data Sharing and Transfers"
    SECTION6 = "Data Retention"
    SECTION7 = "Disclosure of Personal Information"
    SECTION8 = "Security Measures"
    SECTION9 = "Automated Decision-Making and Profiling"
    SECTION10 = "Cookies and Tracking Technologies"
    SECTION11 = "Changes to the Privacy Policy"
    SECTION12 = "Contact Information"


class SectionKeyPoints(BaseModel):
    name: SectionNames = Field(..., title="Section Name")
    key_points: List[str] = Field(..., title="List of Key Points")


SectionList = conlist(SectionKeyPoints, min_length=12, max_length=12)


class Syllabus(BaseModel):
    sections: SectionList = Field(..., title="List of Sections")


class SectionContent(BaseModel):
    name: SectionNames = Field(..., title="Section Name")
    content: str = Field(..., title="Section Content")


class Judge(BaseModel):

    name: SectionNames = Field(..., title="Section Name")

    suggestions: str = Field(
        ...,
        title="Suggestions for improvement",
        description="Leave empty if it's comments instead of suggestions.",
    )


class Judges(BaseModel):

    judges: List[Judge] = Field(
        ...,
        title="Judges",
        description="Judges for the sections.",
    )


class RegulationRegions(str, Enum):
    US = "United States"
    USCA = "California"
    EU = "European Union"
    UK = "United Kingdom"
    CA = "Canada"
    AU = "Australia"
    IN = "India"
    SG = "Singapore"
    JP = "Japan"
    KR = "South Korea"
    BR = "Brazil"
    ZA = "South Africa"
    OTHER = "Other"


class SelectedRegions(BaseModel):
    regions: List[RegulationRegions] = Field(
        ...,
        title="List of Selected Regions",
        description=("List of selected regions. "
                     "Note that some regions could be mutually inclusive."))
