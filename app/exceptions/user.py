from typing import Any

from fastapi import HTTPException, status


class UserIdInvalidException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = [{"msg": "Неверный тип id пользователя", "type": "event.user.invalid"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class UserNotCreatorException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: Any = [{"msg": "Пользователь не владелец события", "type": "event.user.not_creator"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
