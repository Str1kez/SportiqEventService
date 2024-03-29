import json
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.schema.type import TypesResponse
from app.tools import redis_cache
from app.usecase import select_all_types


router = APIRouter(tags=["Type"], prefix="/type")

db_session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", status_code=status.HTTP_200_OK, summary="List of sport types")
async def get_sport_types(session: db_session, cache: redis_cache) -> TypesResponse:
    in_cache = await cache.get("/type")
    if in_cache:
        return json.loads(in_cache)
    response = await select_all_types(session)
    await cache.set("/type", response.json(by_alias=True), expire=600)
    return response
