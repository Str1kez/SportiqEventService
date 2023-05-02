from datetime import timedelta

from app.config import DefaultSettings
from app.db.models import Event, EventStatus
from app.exceptions import EventReadOnlyException, HourHandicapException, UserNotCreatorException
from app.tools import is_handicap


def check_permission(event: Event, user_id: str) -> None:
    if event.creator_id != user_id:
        raise UserNotCreatorException


def check_status(event: Event) -> None:
    if event.status != EventStatus.planned:
        raise EventReadOnlyException


def check_timing(event: Event) -> None:
    settings = DefaultSettings()
    if not is_handicap(event.starts_at, timedelta(hours=settings.HANDICAP_HOURS)):
        raise HourHandicapException
