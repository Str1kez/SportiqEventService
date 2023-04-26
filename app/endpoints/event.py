from typing import Annotated

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.db.models import EventStatus
from app.exceptions import (
    EventIdInvalidException,
    EventNotFoundException,
    EventTypeNotFoundException,
    UserIdInvalidException,
)
from app.schema import EventCreateRequest, EventListMapResponse, EventResponse, EventUpdateRequest
from app.tools import time_check
from app.usecase import (
    create_event,
    delete_event_by_id,
    select_event_by_id,
    select_event_list_for_map,
    update_event_by_id,
)


router = APIRouter(tags=["Event"], prefix="/event")

user_id_from_header = Annotated[str, Header(..., alias="User")]
db_session = Annotated[AsyncSession, Depends(get_session)]
event_id = Annotated[str, Path(alias="id")]


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def new_event(
    event_data: EventCreateRequest,
    user_id: user_id_from_header,
    session: db_session,
) -> EventResponse:
    time_check(event_data.starts_at, event_data.ends_at)
    try:
        event = await create_event(event_data, user_id, session)
    except IntegrityError:
        raise EventTypeNotFoundException
    except DBAPIError:
        raise UserIdInvalidException
    return event


@router.get("/map", response_model=EventListMapResponse, status_code=status.HTTP_200_OK)
async def get_event_list_by_query(
    session: db_session,
    city: str = Query(...),
    type_: str = Query(None, alias="type"),
    status: EventStatus = Query(None),
) -> EventListMapResponse:
    # try:
    event_list = await select_event_list_for_map(city, type_, status, session)
    # except IntegrityError:
    #     raise EventTypeNotFoundException
    return event_list


@router.get("/{id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def get_event(id_: event_id, session: db_session) -> EventResponse:
    try:
        event = await select_event_by_id(id_, session)
    except NoResultFound:
        raise EventNotFoundException
    except DBAPIError:
        raise EventIdInvalidException
    return event


@router.patch("/{id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def update_event(
    event_data: EventUpdateRequest, id_: event_id, user_id: user_id_from_header, session: db_session
) -> EventResponse:
    time_check(event_data.starts_at, event_data.ends_at)
    try:
        event = await update_event_by_id(event_data, id_, user_id, session)
    except NoResultFound:
        raise EventNotFoundException
    except DBAPIError:
        raise EventIdInvalidException
    return event


@router.delete("/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id_: event_id, user_id: user_id_from_header, session: db_session) -> None:
    try:
        await delete_event_by_id(id_, user_id, session)
    except DBAPIError:
        return
