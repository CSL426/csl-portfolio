# Single-image build for Cloud Run: Vite static site + FastAPI in one container.
# Cloud Run runs one container per service, so the SPA is served by FastAPI
# (SpaStaticFiles) instead of a separate nginx container.
FROM node:22-alpine AS builder
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@9.15.9 --activate

COPY pnpm-workspace.yaml package.json pnpm-lock.yaml .npmrc* ./
COPY apps/web/package.json apps/web/
RUN pnpm install --frozen-lockfile --filter @spark/web

COPY apps/web apps/web
RUN pnpm --filter @spark/web build

FROM python:3.12-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STATIC_DIR=/srv/static

WORKDIR /srv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

COPY apps/api/pyproject.toml apps/api/uv.lock* ./
COPY apps/api/server ./server
RUN uv sync --frozen --no-dev || uv sync --no-dev

ENV PATH="/srv/.venv/bin:$PATH"

COPY --from=builder /app/apps/web/dist ${STATIC_DIR}

EXPOSE 8080
# Cloud Run injects PORT (default 8080); shell form so it expands at start.
CMD uvicorn server.main:app --host 0.0.0.0 --port ${PORT:-8080}
