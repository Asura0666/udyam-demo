from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import UdyamApplication, VerificationAttempt
import hashlib
import uuid


class AadhaarService:
    async def send_otp(
        self,
        aadhaar_number: str,
        entrepreneur_name: str,
        consent: bool,
        session: AsyncSession,
    ):
        # Mask & hash Aadhaar for storage
        aadhaar_last4 = aadhaar_number[-4:]
        aadhaar_hash = hashlib.sha256(aadhaar_number.encode()).hexdigest()

        app = UdyamApplication(
            entrepreneur_name=entrepreneur_name,
            aadhaar_last4=aadhaar_last4,
            aadhaar_hash=aadhaar_hash,
            aadhaar_consent=consent,
            status="draft",
        )

        session.add(app)
        await session.commit()
        await session.refresh(app)

        # Simulate OTP sending (fake)
        transaction_id = str(uuid.uuid4())

        attempt = VerificationAttempt(
            app_id=app.id,
            kind="aadhaar_otp",
            success=True,
            payload={"transaction_id": transaction_id, "otp_sent": True},
        )

        session.add(attempt)
        await session.commit()

        return {
            "transactionId": transaction_id,
            "otpSentTo": f"****{aadhaar_last4}",
            "appId": str(app.id),
        }

    async def verify_otp(
        self, app_id: uuid.UUID, transaction_id: str, otp: str, session: AsyncSession
    ):
        # Simulated success
        stmt = select(UdyamApplication).where(UdyamApplication.id == app_id)
        app = (await session.exec(stmt)).first()

        if not app:
            raise ValueError("Application not found")

        app.aadhaar_verified = True
        app.aadhaar_verified_at = datetime.utcnow()
        await session.commit()

        attempt = VerificationAttempt(
            app_id=app.id,
            kind="aadhaar_otp",
            success=True,
            payload={"transaction_id": transaction_id, "otp": otp},
            message="OTP verified successfully",
        )
        session.add(attempt)
        await session.commit()

        return {"verified": True, "appId": str(app.id)}
