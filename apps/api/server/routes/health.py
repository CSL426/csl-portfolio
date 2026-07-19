from typing import Any

from fastapi import APIRouter

from server import __version__
from server.agents import registry
from server.core.config import get_settings

router = APIRouter(tags=["meta"])


@router.get("/health")
async def health() -> dict[str, Any]:
    settings = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "env": settings.app_env,
        "line_configured": settings.line_configured,
        "agents": registry.names(),
        "default_agent": settings.default_agent,
    }
