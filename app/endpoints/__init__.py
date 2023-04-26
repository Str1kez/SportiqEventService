from app.endpoints.event import router as event_router
from app.endpoints.status import router as status_router
from app.endpoints.type import router as type_router


routes = [event_router, type_router, status_router]

__all__ = ["routes"]
