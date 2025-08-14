from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class YesNo(str, Enum):
    YES = "1"
    NO = "2"

class GSTINStatus(str, Enum):
    YES = "1"
    NO = "2"
    EXEMPTED = "3"

class FinalFormRequest(BaseModel):
    entrepreneurName: str = Field(..., max_length=255)
    typeOfOrganisation: str = Field(..., max_length=50)
    dobOrDoi: date
    previousYearITR: YesNo
    hasGSTIN: GSTINStatus

    @field_validator("dobOrDoi", mode="before")
    @classmethod
    def parse_ddmmyyyy(cls, v):
        """Convert dd-mm-yyyy to date object."""
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d-%m-%Y").date()
            except ValueError:
                pass
        return v

class FinalFormResponse(BaseModel):
    registrationId: str
    status: str
