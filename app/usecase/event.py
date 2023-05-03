from sqlalchemy import insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from .permission_checker import check_permission, check_status, check_timing
from app.config.settings import DefaultSettings
from app.db.models import Event, EventStatus
from app.schema import EventCreateRequest, EventListMapResponse, EventResponse, EventUpdateRequest


async def create_event(event_data: EventCreateRequest, user_id: str, session: AsyncSession) -> EventResponse:
    event_db_dict = event_data.dict(by_alias=False) | {"creator_id": user_id}
    db_execution = await session.execute(insert(Event).returning(Event), [event_db_dict])
    event_db = db_execution.scalar_one()
    await session.commit()
    return EventResponse.from_orm(event_db)


async def select_event_by_id(event_id: str, session: AsyncSession) -> EventResponse:
    db_query = select(Event).where(Event.id_ == event_id).where(Event.is_active == True)
    db_execution = await session.execute(db_query)
    event_db = db_execution.scalar_one()
    return EventResponse.from_orm(event_db)


async def select_event_list_for_map(
    city: str, type_: str | None, status: EventStatus | None, session: AsyncSession
) -> EventListMapResponse:
    db_query = select(Event).where(Event.city == city).where(Event.is_active == True)
    if type_ is not None:
        db_query = db_query.where(Event.type_ == type_)

    if status is not None:
        db_query = db_query.where(Event.status == status)
    else:
        db_query = db_query.where(Event.status != EventStatus.deleted).where(Event.status != EventStatus.completed)

    db_execution = await session.execute(db_query)
    events_db = db_execution.scalars().all()
    result = EventListMapResponse()
    result.insert_from_orm(events_db)
    return result


async def update_event_by_id(
    event_data: EventUpdateRequest, event_id: str, user_id: str, session: AsyncSession
) -> EventResponse:
    db_query = select(Event).where(Event.id_ == event_id).where(Event.is_active == True)
    db_execution = await session.execute(db_query)
    event_db = db_execution.scalar_one()
    check_permission(event_db, user_id)
    check_status(event_db)
    check_timing(event_db)
    event_db.__dict__.update(event_data.dict(exclude_none=True))

    db_query = update(Event).where(Event.id_ == event_db.id_).values(**event_data.dict(exclude_none=True))
    await session.execute(db_query)
    await session.commit()

    return EventResponse.from_orm(event_db)


async def delete_event_by_id(event_id: str, user_id: str, session: AsyncSession) -> None:
    db_query = select(Event).where(Event.id_ == event_id).where(Event.is_active == True)
    db_execution = await session.execute(db_query)
    event_db = db_execution.scalar_one()
    check_permission(event_db, user_id)
    check_status(event_db)
    check_timing(event_db)
    db_query = update(Event).where(Event.id_ == event_id).values({"status": EventStatus.deleted.value})
    await session.execute(db_query)
    await session.commit()
