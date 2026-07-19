FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    API_PORT=8000

WORKDIR /srv

# uv: fast dependency manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Install dependencies first so layer caches independently of source changes.
# README is referenced by some hatchling builds; server is required by [tool.hatch...packages]
COPY pyproject.toml uv.lock* ./
COPY server ./server
RUN uv sync --frozen --no-dev || uv sync --no-dev

ENV PATH="/srv/.venv/bin:$PATH"

# EXPOSE is documentation-only; actual port is $API_PORT at runtime.
EXPOSE 8000

# Shell form so $API_PORT expands at container start (exec form can't).
CMD uvicorn server.main:app --host 0.0.0.0 --port ${API_PORT}
