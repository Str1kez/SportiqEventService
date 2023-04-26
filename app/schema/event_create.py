from datetime import datetime

from pydantic import BaseModel, Field

from app.db.models import EventStatus


class EventCreateRequest(BaseModel):
    title: str = Field(..., min_length=5)
    description: str | None
    address: str | None = Field(min_length=5)
    city: str
    latitude: float
    longitude: float
    starts_at: datetime = Field(..., alias="startsAt")
    ends_at: datetime = Field(..., alias="endsAt")
    type_: str = Field(..., alias="type")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class EventCreateResponse(EventCreateRequest):
    _id: str = Field(..., alias="id")
    status: EventStatus
    creator_id: str = Field(..., alias="creatorId")
    is_active: bool = Field(..., alias="isActive")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
