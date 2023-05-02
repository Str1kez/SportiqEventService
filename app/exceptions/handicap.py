from typing import Any

from fastapi import HTTPException, status

from app.config import DefaultSettings


settings = DefaultSettings()


class HourHandicapException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = [
            {"msg": f"До старта должно быть не меньше {settings.HANDICAP_HOURS} ч.", "type": "event.handicap"}
        ],
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


class EventDurationException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = [
            {
                "msg": f"Событие должно длиться не меньше {settings.EVENT_DURATION_MINUTES} мин.",
                "type": "event.duration",
            }
        ],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
