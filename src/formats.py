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


class Section(BaseModel):
    name: SectionNames = Field(..., title="Section Name")
    key_points: List[str] = Field(..., title="List of Key Points")


SectionList = conlist(Section, min_length=12, max_length=12)


class Syllabus(BaseModel):
    sections: SectionList = Field(..., title="List of Sections")
