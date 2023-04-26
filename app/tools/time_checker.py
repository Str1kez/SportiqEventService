from datetime import datetime, timedelta

from app.config import DefaultSettings
from app.exceptions import HourHandicapException, StartUpException


def __is_handicap(start: datetime, value: timedelta) -> bool:
    return datetime.now(start.tzinfo) + value <= start


def time_check(start: datetime, end: datetime):
    hours = DefaultSettings().HANDICAP_HOURS
    if not __is_handicap(start, timedelta(hours=hours)):
        raise HourHandicapException
    if start >= end:
        raise StartUpException
