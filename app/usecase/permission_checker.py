from app.db.models import Event, EventStatus
from app.exceptions import EventReadOnlyException, UserNotCreatorException


def check_permission(event: Event, user_id: str) -> None:
    if event.creator_id != user_id:
        raise UserNotCreatorException


def check_status(event: Event) -> None:
    if event.status != EventStatus.planned:
        raise EventReadOnlyException
