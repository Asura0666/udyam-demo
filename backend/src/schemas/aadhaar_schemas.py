from pydantic import BaseModel, Field
from uuid import UUID

# ---------- Request Schemas ----------
class AadhaarSendOtpRequest(BaseModel):
    aadhaarNumber: str = Field(
        ...,
        min_length=12,
        max_length=12,
        pattern=r"^\d{12}$"  # use pattern instead of regex in Pydantic v2
    )
    entrepreneurName: str = Field(..., max_length=100)
    consent: bool

class AadhaarVerifyOtpRequest(BaseModel):
    app_id: str
    transaction_id: str
    otp: str = Field(..., min_length=6, max_length=6)

# ---------- Response Schemas ----------
class AadhaarSendOtpResponse(BaseModel):
    transactionId: str
    otpSentTo: str
    appId: str

class AadhaarVerifyOtpResponse(BaseModel):
    verified: bool
    appId: str
