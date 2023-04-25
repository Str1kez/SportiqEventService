from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.config import DefaultSettings
from app.db.storage import Storage
from app.endpoints import routes


def bind_routes(app: FastAPI):
    path_prefix = DefaultSettings().PATH_PREFIX
    for router in routes:
        app.include_router(router, prefix=path_prefix)


def add_cors(app: FastAPI):
    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def on_startup(_: FastAPI):
    kds_db = Storage().get_connection()
    # Some business
    yield


app = FastAPI(lifespan=on_startup, root_path=f"http://{DefaultSettings().APP_HOST}:{DefaultSettings().APP_PORT}")
add_cors(app)
bind_routes(app)


if __name__ == "__main__":
    settings = DefaultSettings()
    run("app.__main__:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True, reload_dirs=["app"])
