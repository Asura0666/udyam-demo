from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date

# ---------- Request Schemas ----------
class PanVerifyRequest(BaseModel):
    appId: UUID
    panNumber: str = Field(
        ...,
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"  # pattern instead of regex
    )
    panHolderName: str = Field(..., max_length=100)
    dobOrDoi: date
    consent: bool

# ---------- Response Schemas ----------
class PanVerifyResponse(BaseModel):
    verified: bool
    appId: str
