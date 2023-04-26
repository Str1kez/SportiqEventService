from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.event import Event
from app.schema import EventCreateRequest, EventCreateResponse


async def create_event(event_data: EventCreateRequest, user_id: str, session: AsyncSession) -> EventCreateResponse:
    event_db_dict = event_data.dict(by_alias=False) | {"creator_id": user_id}
    db_execution = await session.execute(insert(Event).returning(Event), [event_db_dict])
    execution_result = db_execution.scalar_one()
    await session.commit()
    return EventCreateResponse.from_orm(execution_result)
