from datetime import timedelta

from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import EventTypeNotFoundException, HourHandicapException, StartUpException, UserIdInvalidException
from app.schema import EventCreateRequest, EventCreateResponse
from app.tools import is_handicap
from app.usecase import create_event


router = APIRouter(tags=["Event"], prefix="/event")


@router.post("", response_model=EventCreateResponse, status_code=status.HTTP_201_CREATED)
async def new_event(
    event_data: EventCreateRequest,
    user_id: str = Header(..., alias="User"),
    session: AsyncSession = Depends(get_session),
):
    if not is_handicap(event_data.starts_at, timedelta(hours=1)):
        raise HourHandicapException
    if event_data.starts_at >= event_data.ends_at:
        raise StartUpException
    try:
        event = await create_event(event_data, user_id, session)
    except IntegrityError:
        raise EventTypeNotFoundException
    except DBAPIError:
        raise UserIdInvalidException
    return event
