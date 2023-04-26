from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.schema.type import TypesResponse
from app.usecase import select_all_types


router = APIRouter(tags=["Type"], prefix="/type")

db_session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", status_code=status.HTTP_200_OK)
async def get_sport_types(session: db_session) -> TypesResponse:
    return await select_all_types(session)
