from fastapi import APIRouter, Depends, status
from fastapi import File, UploadFile, Form
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.services.ai import AiService
router = APIRouter(tags=["A.I"], prefix="/ai")


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(session: AsyncSession = Depends(get_session), images: List[UploadFile] = File(...), context: str = Form(...), socialMedia: str = Form(...)):
    return await AiService.upload(session, images, context, socialMedia)
