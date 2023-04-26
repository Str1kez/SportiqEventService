from typing import Any

from fastapi import HTTPException, status


class HourHandicapException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = [{"msg": "До старта должно быть не меньше часа", "type": "event.hour_handicap"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class StartUpException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = [{"msg": "Старт должен быть раньше конца", "type": "event.start_ge_end"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
