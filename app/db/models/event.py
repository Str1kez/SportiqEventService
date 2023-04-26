import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import ENUM, FLOAT, TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseId
from app.db import DeclarativeBase


class EventStatus(enum.Enum):
    deleted = "Удалено"
    planned = "Запланировано"
    completed = "Завершено"
    underway = "Идет"


class EventType(DeclarativeBase):
    __tablename__ = "event_type"

    name: Mapped[str] = mapped_column(
        TEXT,
        primary_key=True,
    )
    # events: Mapped[list["Event"]] = relationship("Event", lazy="joined", innerjoin=True, back_populates="type")


class Event(BaseId):
    __tablename__ = "event"

    title: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        doc="Title of event",
    )
    description: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
        doc="Description of event",
    )
    address: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,  # Perhaps need to change
        doc="Address of event",
    )
    city: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        index=True,
        doc="City of event",
    )
    longitude: Mapped[float] = mapped_column(
        "longitude", FLOAT, nullable=False, index=True, doc="Longitude of warehouse"
    )
    latitude: Mapped[float] = mapped_column("latitude", FLOAT, nullable=False, index=True, doc="Latitude of warehouse")
    # index on group of lon and lat
    status: Mapped[EventStatus] = mapped_column(
        ENUM(EventStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        server_default=text(f"'{EventStatus.planned.value}'"),
        index=True,
        doc="Class of event",
    )
    creator_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        # index=True, # if need to get created by user
        doc="Creator of event",
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="DateTime of starting event",
    )
    ends_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="DateTime of ending event",
    )
    type_: Mapped[str] = mapped_column(
        ForeignKey("event_type.name", ondelete="CASCADE"), nullable=False, name="type", doc="Sport type of event"
    )

    # type: Mapped[EventType] = relationship("EventType", lazy="joined", innerjoin=True, back_populates="events")
