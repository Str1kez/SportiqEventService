from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from uvicorn import run

from app.config import DefaultSettings
from app.endpoints import routes


settings = DefaultSettings()


def bind_routes(app: FastAPI):
    path_prefix = settings.PATH_PREFIX
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
    rc = RedisCacheBackend(settings.CACHE_URL)
    caches.set(CACHE_KEY, rc)
    yield
    await close_caches()


app = FastAPI(
    lifespan=on_startup,
    root_path=f"http://{settings.APP_HOST}:{settings.APP_PORT}",
    title="Event Microservice for Sportiq project",
    description="This microservice supports operatinons on events, interaction with subscription microservice via message queue. **All endpoints are available only for authenticated users by API Gateway**",
)
add_cors(app)
bind_routes(app)


if __name__ == "__main__":
    run("app.__main__:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True, reload_dirs=["app"])
