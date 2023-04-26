from typing import Any

from fastapi import HTTPException, status


class EventTypeNotFoundException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = [{"msg": "Тип спорта не существует", "type": "event.type.not_found"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class EventNotFoundException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = [{"msg": "Событие не найдено", "type": "event.not_found"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class EventIdInvalidException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = [{"msg": "Неверный тип id события", "type": "event.id.invalid"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class EventReadOnlyException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = [{"msg": "Событие уже нельзя изменять", "type": "event.status.readonly"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
