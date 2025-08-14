from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.services.aadhaar_service import AadhaarService
from src.schemas.aadhaar_schemas import (
    AadhaarSendOtpRequest,
    AadhaarSendOtpResponse,
    AadhaarVerifyOtpRequest,
    AadhaarVerifyOtpResponse,
)

aadhaar_router = APIRouter()

aadhaar_service = AadhaarService()


@aadhaar_router.post("/send-otp", response_model=AadhaarSendOtpResponse)
async def send_otp(
    payload: AadhaarSendOtpRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Step 1 — Send OTP to the given Aadhaar number.
    """
    try:
        result = await aadhaar_service.send_otp(
            aadhaar_number=payload.aadhaarNumber,
            entrepreneur_name=payload.entrepreneurName,
            consent=payload.consent,
            session=session,
        )
        return AadhaarSendOtpResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@aadhaar_router.post("/verify-otp", response_model=AadhaarVerifyOtpResponse)
async def verify_otp(
    payload: AadhaarVerifyOtpRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Step 2 — Verify the OTP received by the user.
    """
    try:
        result = await aadhaar_service.verify_otp(
            app_id=payload.app_id,
            transaction_id=payload.transaction_id,
            otp=payload.otp,
            session=session,
        )
        return AadhaarVerifyOtpResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
