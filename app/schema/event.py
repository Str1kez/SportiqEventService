from datetime import datetime
from typing import Iterable

from pydantic import BaseModel, Field

from .event_change import EventCreateRequest
from app.db.models import EventStatus


class EventResponse(EventCreateRequest):
    id_: str = Field(..., alias="id")
    status: EventStatus
    creator_id: str = Field(..., alias="creatorId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class EventMapResponse(BaseModel):
    id_: str = Field(..., alias="id")
    title: str = Field(..., min_length=5)
    address: str | None = Field(min_length=5)  # TODO: Убрать мб
    city: str  # TODO: Убрать мб
    latitude: float
    longitude: float
    starts_at: datetime = Field(..., alias="startsAt")
    ends_at: datetime = Field(..., alias="endsAt")
    type_: str = Field(..., alias="type")
    status: EventStatus

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class EventListMapResponse(BaseModel):
    events: list[EventMapResponse] = []

    def insert_from_orm(self, obj: Iterable):
        for o in obj:
            self.events.append(EventMapResponse.from_orm(o))

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
