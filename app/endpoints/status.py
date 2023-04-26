from fastapi import APIRouter, status

from app.db.models.event import EventStatus


router = APIRouter(tags=["Status"], prefix="/status")


@router.get("", status_code=status.HTTP_200_OK)
async def get_available_statuses():
    return {"statuses": list(EventStatus)}
