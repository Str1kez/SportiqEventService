import json
from typing import Annotated

from aio_pika.abc import AbstractChannel
from aio_pika.pool import Pool
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
from app.mq import MQEventType, MQManager, publish_json
from app.schema import EventCreateRequest, EventListMapResponse, EventResponse, EventUpdateRequest
from app.tools import redis_cache, time_check
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
mq_channel_pool = Annotated[Pool[AbstractChannel], Depends(MQManager().get_channel_pool)]


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED, summary="Create event")
async def new_event(
    event_data: EventCreateRequest,
    user_id: user_id_from_header,
    session: db_session,
    mq: mq_channel_pool,
    cache: redis_cache,
) -> EventResponse:
    time_check(event_data.starts_at, event_data.ends_at)
    try:
        event = await create_event(event_data, user_id, session)
    except IntegrityError:
        raise EventTypeNotFoundException
    except DBAPIError:
        raise UserIdInvalidException
    mq_message = json.dumps({"user_id": user_id, "event_id": event.id_})
    await publish_json(mq, "events", mq_message, MQEventType.create)
    await cache.set(f"event/{event.id_}", event.json(by_alias=True), expire=60)
    return event


@router.get("/map", response_model=EventListMapResponse, status_code=status.HTTP_200_OK, summary="Short info for maps")
async def get_event_list_by_query(
    session: db_session,
    cache: redis_cache,
    city: str = Query(...),
    type_: str = Query(None, alias="type"),
    status: EventStatus = Query(None),
) -> EventListMapResponse:
    in_cache = await cache.get(f"event/map:city={city}:type={type_}:status={status}")
    if in_cache:
        return json.loads(in_cache)
    event_list = await select_event_list_for_map(city, type_, status, session)
    await cache.set(f"event/map:city={city}:type={type_}:status={status}", event_list.json(by_alias=True), expire=60)
    return event_list


@router.get(
    "/{id}", response_model=EventResponse, status_code=status.HTTP_200_OK, summary="Full info about single event"
)
async def get_event(id_: event_id, session: db_session, cache: redis_cache) -> EventResponse:
    in_cache = await cache.get(f"event/{id_}")
    if in_cache:
        return json.loads(in_cache)
    try:
        event = await select_event_by_id(id_, session)
    except NoResultFound:
        raise EventNotFoundException
    except DBAPIError:
        raise EventIdInvalidException
    await cache.set(f"event/{id_}", event.json(by_alias=True), expire=60)
    return event


@router.patch("/{id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def update_event(
    event_data: EventUpdateRequest, id_: event_id, user_id: user_id_from_header, session: db_session, cache: redis_cache
) -> EventResponse:
    if event_data.starts_at is not None and event_data.ends_at is not None:
        time_check(event_data.starts_at, event_data.ends_at)
    try:
        event = await update_event_by_id(event_data, id_, user_id, session)
    except NoResultFound:
        raise EventNotFoundException
    except DBAPIError:
        raise EventIdInvalidException
    await cache.set(f"event/{id_}", event.json(by_alias=True), expire=60)
    return event


@router.delete("/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT, summary="Set event as removed")
async def delete_event(
    id_: event_id, user_id: user_id_from_header, session: db_session, cache: redis_cache, mq: mq_channel_pool
) -> None:
    try:
        await delete_event_by_id(id_, user_id, session)
    except NoResultFound:
        raise EventNotFoundException
    except DBAPIError:
        raise EventIdInvalidException
    mq_message = json.dumps({"status": EventStatus.deleted.value, "events": [id_]})
    await publish_json(mq, "events", mq_message, MQEventType.change)
    await cache.delete(f"event/{id_}")
