"""Claude-backed agent (Anthropic Messages API).

Keeps one conversation per `(source, user_id)` in memory, like the ADK agent.
History is append-only: each assistant turn is stored as the full
`response.content` (thinking and fallback blocks included) and earlier turns
are never edited or trimmed. When a conversation grows past
`claude_max_turns`, it is dropped and the next message starts a new one.
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Final, Literal, cast

from server.agents.base import AgentContext, AgentReply, BaseAgent
from server.core.config import get_settings
from server.core.logging import get_logger

if TYPE_CHECKING:
    from anthropic import AsyncAnthropic
    from anthropic.types.beta import BetaMessageParam

logger = get_logger(__name__)

# `fallbacks: "default"` re-runs a request that a safety classifier declined on
# Anthropic's recommended substitute model, inside the same call.
_FALLBACK_BETA: Final[Literal["server-side-fallback-2026-07-01"]] = (
    "server-side-fallback-2026-07-01"
)


class ClaudeAgent(BaseAgent):
    name = "claude"

    def __init__(self, client: AsyncAnthropic | None = None) -> None:
        self.settings = get_settings()
        self._client = client
        self._histories: dict[str, list[BetaMessageParam]] = {}
        self._locks: dict[str, asyncio.Lock] = {}

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
            timeout=60.0,
        )
        return self._client

    async def handle(self, ctx: AgentContext) -> AgentReply:
        client = self._ensure_client()
        if client is None:
            return AgentReply(text="（Claude 尚未設定：請在 .env 填入 ANTHROPIC_API_KEY）")

        import anthropic

        session_id = f"{ctx.source}:{ctx.user_id}"
        lock = self._locks.setdefault(session_id, asyncio.Lock())

        async with lock:
            history = self._histories.get(session_id, [])
            if len(history) >= self.settings.claude_max_turns * 2:
                history = []  # start over rather than editing earlier turns
            messages: list[BetaMessageParam] = [
                *history,
                {"role": "user", "content": ctx.message},
            ]

            try:
                response = await client.beta.messages.create(
                    model=self.settings.claude_model,
                    max_tokens=self.settings.claude_max_tokens,
                    system=self.settings.claude_instruction,
                    messages=messages,
                    output_config={"effort": self.settings.claude_effort},
                    betas=[_FALLBACK_BETA],
                    fallbacks="default",
                )
            except anthropic.AuthenticationError:
                logger.error("claude_auth_failed", session_id=session_id)
                return AgentReply(text="（Claude 金鑰無效，請檢查 ANTHROPIC_API_KEY）")
            except anthropic.RateLimitError:
                logger.warning("claude_rate_limited", session_id=session_id)
                return AgentReply(text="（Claude 目前請求過多，請稍後再試）")
            except anthropic.APIStatusError as e:
                logger.exception("claude_api_error", session_id=session_id, status=e.status_code)
                return AgentReply(text="（Claude 執行錯誤，請查看伺服器 log）")
            except anthropic.APIConnectionError:
                logger.exception("claude_connection_error", session_id=session_id)
                return AgentReply(text="（無法連線到 Claude，請稍後再試）")

            if response.stop_reason == "refusal":
                category = response.stop_details.category if response.stop_details else None
                logger.info("claude_refused", session_id=session_id, category=category)
                # Not stored: the next turn continues from the last good exchange.
                return AgentReply(text="（這個問題我沒辦法回答，換個方式問問看？）")

            # Replay the response blocks exactly as returned (the SDK accepts them
            # as input); the param TypedDict only lists the dict forms.
            assistant = cast("BetaMessageParam", {"role": "assistant", "content": response.content})
            self._histories[session_id] = [*messages, assistant]

        text = "".join(b.text for b in response.content if b.type == "text").strip()
        return AgentReply(
            text=text or "（模型沒有回覆內容）",
            extra={"model": response.model},
        )
