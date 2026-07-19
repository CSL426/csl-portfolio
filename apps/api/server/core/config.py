from functools import cached_property, lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Walk up from this file (server/core/config.py) to find env files.
# pydantic-settings reads tuples in order; later entries override earlier ones —
# so local `apps/api/.env` wins over root `.env` if both exist.
# In the Docker image the tree is shallow (/srv/server/...), so the repo root
# may not exist — fall back to the API dir; missing env files are ignored.
_API_DIR = Path(__file__).resolve().parents[2]
_REPO_ROOT = _API_DIR.parents[1] if len(_API_DIR.parents) > 1 else _API_DIR
_ENV_FILES = (_REPO_ROOT / ".env", _API_DIR / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILES,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = Field(default="dev", description="dev | prod")
    log_level: str = Field(default="INFO")

    # Set in the Cloud Run image (STATIC_DIR); unset in local dev where Vite serves the SPA.
    static_dir: str | None = Field(default=None)

    cors_origins: list[str] | None = Field(default=None)

    line_channel_secret: str | None = Field(default=None)
    line_channel_access_token: str | None = Field(default=None)

    default_agent: str = Field(default="echo")

    # Google ADK / Gemini (AI Studio key — get from https://aistudio.google.com/app/apikey)
    google_api_key: str | None = Field(default=None)
    adk_model: str = Field(default="gemini-3.1-flash")
    adk_app_name: str = Field(default="portfolio-server")
    adk_instruction: str = Field(
        default=(
            "You are Spark, the AI assistant on Liao Chi-Shun's portfolio site. "
            "Be concise, friendly, and bilingual (Traditional Chinese + English). "
            "When asked about Spark's background, defer to the resume on the site."
        )
    )

    @cached_property
    def effective_cors_origins(self) -> list[str]:
        """Use explicit cors_origins if set; otherwise default to Vite dev URLs."""
        return self.cors_origins or [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]

    @property
    def line_configured(self) -> bool:
        return bool(self.line_channel_secret and self.line_channel_access_token)

    @property
    def adk_configured(self) -> bool:
        return bool(self.google_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
