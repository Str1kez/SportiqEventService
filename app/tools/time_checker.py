from datetime import datetime, timedelta

from app.config import DefaultSettings
from app.exceptions import EventDurationException, HourHandicapException, StartUpException


def is_handicap(start: datetime, value: timedelta) -> bool:
    return datetime.now(start.tzinfo) + value <= start


def time_check(start: datetime, end: datetime):
    settings = DefaultSettings()
    if not is_handicap(start, timedelta(hours=settings.HANDICAP_HOURS)):
        raise HourHandicapException
    if start >= end:
        raise StartUpException
    if end - timedelta(minutes=settings.EVENT_DURATION_MINUTES) < start:
        raise EventDurationException
