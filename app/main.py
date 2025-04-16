from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router_with_api_key, api_router_without_api_key
from app.core.config import settings
from app.core.db import init_db


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(_: FastAPI):  # type:ignore[no-untyped-def]
    # await restart_db()
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Register routes
app.include_router(api_router_with_api_key, prefix=settings.API_V1_STR)
app.include_router(api_router_without_api_key, prefix=settings.API_V1_STR)
