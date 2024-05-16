import os
import time
from collections.abc import Awaitable, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.requests import Request
from starlette.responses import Response

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as rooms_router
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(
        application: FastAPI  # noqa: ARG001
) -> AbstractAsyncContextManager[None]:
    redis = aioredis.from_url(settings.redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="hotel-booking")
    yield


app = FastAPI(lifespan=lifespan)

if os.environ.get("ENV") == "production":
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


@app.get("/sentry-debug")
async def trigger_error() -> None:
    division_by_zero = 1 / 0  # noqa: F841


app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)

app.include_router(pages_router)
app.include_router(images_router)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"]
)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
admin.add_view(BookingAdmin)


@app.middleware("http")
async def add_process_time_header(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })

    return response

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
