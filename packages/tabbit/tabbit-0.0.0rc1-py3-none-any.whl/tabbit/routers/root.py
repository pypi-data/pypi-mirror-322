from __future__ import annotations

from fastapi import APIRouter

from tabbit.routers.api.root import api_router
from tabbit.schemas.root import ServerHealthResponse

root_router = APIRouter(prefix="")
root_router.include_router(api_router)


@root_router.get("/ping")
async def ping() -> ServerHealthResponse:
    """Server healthcheck."""
    return ServerHealthResponse()
