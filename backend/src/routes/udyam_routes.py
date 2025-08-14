from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.schemas.udyam_schemas import FinalFormRequest, FinalFormResponse
from src.services.udyam_service import UdyamService

udyam_router = APIRouter()

@udyam_router.post("/{app_id}/submit", response_model=FinalFormResponse)
async def submit_final_form(
    app_id: UUID,
    request: FinalFormRequest,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await UdyamService().submit_registration(app_id, request.model_dump(), session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
