import hashlib
import re
import secrets
from functools import lru_cache
from typing import Any, Final

from fastapi import APIRouter, HTTPException, Request, Response, status

from server.agents import EMPTY_MESSAGE_REPLY, AgentContext, registry
from server.core.config import get_settings
from server.core.rate_limit import RateLimiter
from server.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

SESSION_COOKIE: Final = "portfolio_session"
_SESSION_TOKEN = re.compile(r"[A-Za-z0-9_-]{43}")  # shape of token_urlsafe(32)


class _ChatLimits:
    def __init__(self) -> None:
        settings = get_settings()
        self.session = RateLimiter(settings.chat_limit_per_session_per_minute, 60)
        self.ip = RateLimiter(settings.chat_limit_per_ip_per_minute, 60)
        self.daily = RateLimiter(settings.chat_limit_per_day, 86_400)

    def allow(self, session_key: str, ip: str) -> bool:
        # Daily last: requests refused per session or IP must not use up the
        # budget that everyone else shares.
        return self.session.allow(session_key) and self.ip.allow(ip) and self.daily.allow("all")


@lru_cache
def get_chat_limits() -> _ChatLimits:
    return _ChatLimits()


def _client_ip(request: Request) -> str:
    # The proxy in front (Cloud Run, or nginx under docker compose) appends the
    # address it saw, so only the last entry is trustworthy; earlier ones are
    # whatever the client chose to send.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.rsplit(",", 1)[-1].strip()
    return request.client.host if request.client else "unknown"


def _user_id(token: str) -> str:
    # The token is a credential, and user ids end up in logs.
    return hashlib.sha256(token.encode()).hexdigest()[:32]


def _session_user_id(request: Request, response: Response) -> str:
    """Identify the visitor by a server-issued cookie, never by a client-chosen id."""
    token = request.cookies.get(SESSION_COOKIE)
    if token is None or not _SESSION_TOKEN.fullmatch(token):
        token = secrets.token_urlsafe(32)
        response.set_cookie(
            SESSION_COOKIE,
            token,
            path="/api/chat",
            httponly=True,
            samesite="lax",
            # Behind Cloud Run the app itself only ever sees plain HTTP.
            secure=request.headers.get("x-forwarded-proto", request.url.scheme) == "https",
        )
    return _user_id(token)


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request, response: Response) -> ChatResponse:
    settings = get_settings()
    message = req.message
    if req.agent:
        agent = registry.get(req.agent)
        if agent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unknown agent: {req.agent}. Available: {registry.names()}",
            )
    else:
        # Same convention as the LINE webhook: a leading `/<agent>` picks the agent.
        agent, message = registry.resolve(message, default=settings.default_agent)

    if not message.strip():
        return ChatResponse(agent=agent.name, text=EMPTY_MESSAGE_REPLY)

    user_id = _session_user_id(request, response)
    if not get_chat_limits().allow(user_id, _client_ip(request)):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many messages, please try again later.",
        )

    ctx = AgentContext(user_id=user_id, source="web", message=message)
    reply = await agent.handle(ctx)
    return ChatResponse(agent=agent.name, text=reply.text, extra=reply.extra)


@router.delete("/session", status_code=status.HTTP_204_NO_CONTENT)
async def reset_session(request: Request) -> None:
    """Forget this visitor's conversation in every agent."""
    token = request.cookies.get(SESSION_COOKIE)
    if token is None:
        return
    user_id = _user_id(token)
    for name in registry.names():
        agent = registry.get(name)
        if agent is not None:
            await agent.reset("web", user_id)


@router.get("/agents")
async def list_agents() -> dict[str, Any]:
    return {"agents": registry.names(), "default": get_settings().default_agent}
