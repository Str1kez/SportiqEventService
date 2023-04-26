from datetime import datetime, timedelta


def is_handicap(start: datetime, value: timedelta) -> bool:
    return datetime.now(start.tzinfo) + value <= start
