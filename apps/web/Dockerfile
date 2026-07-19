FROM node:22-alpine AS builder
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@9.15.9 --activate

COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile || pnpm install

COPY . .
RUN pnpm build

FROM nginx:1.27-alpine AS runner

# nginx:alpine's docker-entrypoint runs envsubst on /etc/nginx/templates/*.template
# at container start and writes the result to /etc/nginx/conf.d/ — see
# https://hub.docker.com/_/nginx ("Using environment variables in nginx configuration").
# We restrict substitution to our two vars so $host, $uri, etc. survive untouched.
ENV NGINX_ENVSUBST_TEMPLATE_DIR=/etc/nginx/templates \
    NGINX_ENVSUBST_TEMPLATE_SUFFIX=.template \
    NGINX_ENVSUBST_OUTPUT_DIR=/etc/nginx/conf.d \
    NGINX_ENVSUBST_FILTER='^(API_UPSTREAM|SERVER_NAME|NGINX_PORT)$' \
    API_UPSTREAM=api:8000 \
    SERVER_NAME=_ \
    NGINX_PORT=80

# Default site shipped in the image conflicts with our rendered one — drop it.
RUN rm /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:${NGINX_PORT}/healthz || exit 1

EXPOSE 80
# Keep default CMD — base image's docker-entrypoint handles envsubst before launching nginx.
