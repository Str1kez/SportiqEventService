from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import EventType
from app.schema.type import TypesResponse


async def select_all_types(session: AsyncSession) -> TypesResponse:
    db_execution = await session.execute(select(EventType.name))
    execution_result = db_execution.scalars().all()
    result = TypesResponse()
    for type_ in execution_result:
        result.types.append(type_)
    return result
