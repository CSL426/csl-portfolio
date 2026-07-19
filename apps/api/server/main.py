from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server import __version__
from server.core.config import get_settings
from server.core.logging import configure_logging, get_logger
from server.core.static_files import SpaStaticFiles
from server.routes import chat, health, webhook


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    logger = get_logger("server.routes")
    logger.info(
        "api_starting",
        env=settings.app_env,
        line_configured=settings.line_configured,
    )
    yield
    logger.info("api_shutdown")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Portfolio API",
        version=__version__,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.effective_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(webhook.router, prefix="/api")

    # Mounted last so /api/* routes win; only active when the SPA build is baked in.
    if settings.static_dir and Path(settings.static_dir).is_dir():
        app.mount(
            "/",
            SpaStaticFiles(directory=settings.static_dir, html=True),
            name="spa",
        )
    return app


app = create_app()
