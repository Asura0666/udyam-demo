
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.schemas.pan_schemas import PanVerifyRequest, PanVerifyResponse
from src.services.pan_service import PanService

pan_router = APIRouter()

@pan_router.post("/verify", response_model=PanVerifyResponse)
async def verify_pan(
    request: PanVerifyRequest,
    session: AsyncSession = Depends(get_session)
):
    service = PanService()
    try:
        result = await service.verify_pan(
            app_id=request.appId,
            pan_number=request.panNumber,
            pan_holder_name=request.panHolderName,
            dob_or_doi=request.dobOrDoi,
            consent=request.consent,
            session=session
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
