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


class UserIdInvalidException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = [{"msg": "Неверный тип id пользователя", "type": "event.user.invalid"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
