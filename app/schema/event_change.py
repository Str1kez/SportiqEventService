from datetime import datetime

from pydantic import BaseModel, Field, root_validator


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


class EventUpdateRequest(BaseModel):
    title: str = Field(None, min_length=5)
    description: str | None
    starts_at: datetime = Field(None, alias="startsAt")
    ends_at: datetime = Field(None, alias="endsAt")

    @root_validator(skip_on_failure=True)
    @classmethod
    def both_or_nothing(cls, values):
        s, e = values.get("starts_at"), values.get("ends_at")
        if s is None and e is None:
            return values
        if s is not None and e is not None:
            return values
        raise ValueError("startsAt and endsAt must be provided together")

    class Config:
        allow_population_by_field_name = True
