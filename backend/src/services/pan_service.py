from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import UdyamApplication, VerificationAttempt
import hashlib


class PanService:
    async def verify_pan(
        self,
        app_id,
        pan_number,
        pan_holder_name,
        dob_or_doi,
        consent,
        session: AsyncSession,
    ):
        stmt = select(UdyamApplication).where(UdyamApplication.id == app_id)
        app = (await session.exec(stmt)).first()
        if not app:
            raise ValueError("Application not found")

        pan_masked = pan_number[:5] + "*****" + pan_number[-1:]
        pan_hash = hashlib.sha256(pan_number.encode()).hexdigest()

        app.pan_masked = pan_masked
        app.pan_hash = pan_hash
        app.pan_holder_name = pan_holder_name
        app.dob_or_doi = dob_or_doi
        app.pan_verified = True
        app.pan_verified_at = datetime.utcnow()
        await session.commit()

        attempt = VerificationAttempt(
            app_id=app.id,
            kind="pan",
            success=True,
            payload={"pan_number": pan_masked},
            message="PAN verified (simulated)",
        )
        session.add(attempt)
        await session.commit()

        return {"verified": True, "appId": str(app.id)}
