from datetime import datetime

from sqlalchemy import BOOLEAN, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.db import DeclarativeBase


class BaseId(DeclarativeBase):
    __abstract__ = True
    __tablename__ = None

    _id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        server_default=func.uuid6(),
        name="id",
        doc=f"Unique index of {__tablename__}",
    )
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        server_default=expression.true(),
        nullable=False,
        doc="Is active.",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="DateTime of creation",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="DateTime of changes",
    )
