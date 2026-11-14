"""Claude-backed agent (Anthropic Messages API).

Keeps one conversation per `(source, user_id)` in memory, like the ADK agent.
History is append-only: each assistant turn is stored as the full
`response.content` (thinking blocks included) and earlier turns are never edited
or trimmed. When a conversation grows past `claude_max_turns`, it is dropped and
the next message starts a new one.

Idle sessions expire after `claude_session_ttl_seconds`, and at most
`claude_max_sessions` are kept, so a public endpoint cannot grow memory forever.
"""

from __future__ import annotations

import asyncio
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final, cast

from server.agents.base import AgentContext, AgentReply, BaseAgent
from server.core.config import get_settings
from server.core.logging import get_logger
from server.core.text import to_traditional

if TYPE_CHECKING:
    from anthropic import AsyncAnthropic
    from anthropic.types import MessageParam

logger = get_logger(__name__)

# The SDK retries timeouts too, so the worst case is about
# timeout * (retries + 1). A LINE reply token should not wait much longer.
_TIMEOUT_SECONDS: Final = 15.0
_MAX_RETRIES: Final = 1


@dataclass
class _Session:
    last_used: float
    history: list[MessageParam] = field(default_factory=list)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


class ClaudeAgent(BaseAgent):
    name = "claude"

    def __init__(
        self,
        client: AsyncAnthropic | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.settings = get_settings()
        self._client = client
        self._clock = clock
        self._sessions: OrderedDict[str, _Session] = OrderedDict()

    def _ensure_client(self) -> AsyncAnthropic | None:
        if self._client is not None:
            return self._client
        if not self.settings.claude_configured:
            return None

        from anthropic import AsyncAnthropic

        # Only keys that are not scoped to one workspace need this header.
        headers = (
            {"anthropic-workspace-id": self.settings.anthropic_workspace_id}
            if self.settings.anthropic_workspace_id
            else None
        )
        self._client = AsyncAnthropic(
            api_key=self.settings.anthropic_api_key,
            default_headers=headers,
            timeout=_TIMEOUT_SECONDS,
            max_retries=_MAX_RETRIES,
        )
        return self._client

    def _session(self, session_id: str) -> _Session:
        now = self._clock()
        session = self._sessions.get(session_id)
        if session is None:
            session = _Session(last_used=now)
            self._sessions[session_id] = session
        session.last_used = now
        self._sessions.move_to_end(session_id)

        # Oldest first, so the loop can stop at the first session worth keeping.
        for sid, candidate in list(self._sessions.items()):
            expired = now - candidate.last_used > self.settings.claude_session_ttl_seconds
            over_capacity = len(self._sessions) > self.settings.claude_max_sessions
            if not expired and not over_capacity:
                break
            if not candidate.lock.locked():
                del self._sessions[sid]
        return session

    async def reset(self, source: str, user_id: str) -> None:
        # A request still in flight keeps its own _Session object, so its reply
        # lands on the discarded object and cannot bring the history back.
        self._sessions.pop(f"{source}:{user_id}", None)

    async def handle(self, ctx: AgentContext) -> AgentReply:
        client = self._ensure_client()
        if client is None:
            # Visitors see this, so keep setup details in the log.
            logger.error("claude_not_configured", hint="set ANTHROPIC_API_KEY")
            return AgentReply(text="（Claude 目前無法使用，請稍後再試）")

        import anthropic

        session_id = f"{ctx.source}:{ctx.user_id}"
        session = self._session(session_id)

        async with session.lock:
            history = session.history
            if len(history) >= self.settings.claude_max_turns * 2:
                history = []  # start over rather than editing earlier turns
            messages: list[MessageParam] = [
                *history,
                {"role": "user", "content": ctx.message},
            ]

            try:
                response = await client.messages.create(
                    model=self.settings.claude_model,
                    max_tokens=self.settings.claude_max_tokens,
                    # Its own breakpoint lets every visitor share the system prompt;
                    # the automatic one below only records the end of each conversation.
                    system=[
                        {
                            "type": "text",
                            "text": self.settings.claude_instruction,
                            "cache_control": {"type": "ephemeral"},
                        }
                    ],
                    messages=messages,
                    output_config={"effort": self.settings.claude_effort},
                    # Caches up to the last block, so a visitor's earlier turns are reused
                    # on the next one. Five minutes; a one-hour write costs twice as much.
                    cache_control={"type": "ephemeral"},
                )
            except anthropic.AuthenticationError:
                logger.error("claude_auth_failed", session_id=session_id)
                return AgentReply(text="（Claude 目前無法使用，請稍後再試）")
            except anthropic.RateLimitError:
                logger.warning("claude_rate_limited", session_id=session_id)
                return AgentReply(text="（Claude 目前請求過多，請稍後再試）")
            except anthropic.APIStatusError as e:
                logger.exception("claude_api_error", session_id=session_id, status=e.status_code)
                return AgentReply(text="（Claude 執行錯誤，請查看伺服器 log）")
            except anthropic.APIConnectionError:
                # APITimeoutError is a subclass, so timeouts end up here too.
                logger.exception("claude_connection_error", session_id=session_id)
                return AgentReply(text="（無法連線到 Claude，請稍後再試）")

            usage = response.usage
            logger.info(
                "claude_usage",
                session_id=session_id,
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens,
                cache_read=usage.cache_read_input_tokens or 0,
                cache_write=usage.cache_creation_input_tokens or 0,
            )

            if response.stop_reason == "refusal":
                category = response.stop_details.category if response.stop_details else None
                logger.info("claude_refused", session_id=session_id, category=category)
                # Not stored: the next turn continues from the last good exchange.
                return AgentReply(text="（這個問題我沒辦法回答，換個方式問問看？）")

            # Replay the response blocks exactly as returned (the SDK accepts them
            # as input); the param TypedDict only lists the dict forms.
            assistant = cast("MessageParam", {"role": "assistant", "content": response.content})
            session.history = [*messages, assistant]

        # Only the visible text changes: history above must replay the blocks as returned.
        text = to_traditional("".join(b.text for b in response.content if b.type == "text").strip())
        return AgentReply(
            text=text or "（模型沒有回覆內容）",
            extra={"model": response.model},
        )
