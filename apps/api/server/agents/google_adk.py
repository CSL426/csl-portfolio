"""Google ADK-backed agent.

Wraps a `google.adk.agents.LlmAgent` so it speaks our `BaseAgent` interface.
One `LlmAgent` + `InMemoryRunner` instance is shared across users; sessions
are keyed on `(source, user_id)` so LINE and web conversations stay separate.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from server.agents.base import AgentContext, AgentReply, BaseAgent
from server.core.config import get_settings
from server.core.logging import get_logger

if TYPE_CHECKING:
    from google.adk.agents import LlmAgent
    from google.adk.runners import InMemoryRunner

logger = get_logger(__name__)


class GoogleADKAgent(BaseAgent):
    name = "adk"

    def __init__(self) -> None:
        self.settings = get_settings()
        self._llm: LlmAgent | None = None
        self._runner: InMemoryRunner | None = None
        self._sessions: set[str] = set()  # session ids we've initialized

    def _ensure_runner(self) -> bool:
        """Lazily build the LlmAgent + Runner. Returns False if not configured."""

        if self._runner is not None:
            return True
        if not self.settings.adk_configured:
            return False

        # ADK reads GOOGLE_API_KEY from env at LlmAgent construction time.
        if self.settings.google_api_key:
            os.environ.setdefault("GOOGLE_API_KEY", self.settings.google_api_key)

        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner

        self._llm = LlmAgent(
            model=self.settings.adk_model,
            name="spark_agent",
            instruction=self.settings.adk_instruction,
        )
        self._runner = InMemoryRunner(agent=self._llm, app_name=self.settings.adk_app_name)
        return True

    async def _ensure_session(self, session_id: str) -> None:
        assert self._runner is not None
        if session_id in self._sessions:
            return
        existing = await self._runner.session_service.get_session(
            app_name=self.settings.adk_app_name,
            user_id=session_id,
            session_id=session_id,
        )
        if existing is None:
            await self._runner.session_service.create_session(
                app_name=self.settings.adk_app_name,
                user_id=session_id,
                session_id=session_id,
            )
        self._sessions.add(session_id)

    async def handle(self, ctx: AgentContext) -> AgentReply:
        if not self._ensure_runner():
            return AgentReply(
                text="(Google ADK ?芾身摰?????apps/api/.env 閮?GOOGLE_API_KEY)",
            )
        assert self._runner is not None

        from google.genai import types as gtypes

        session_id = f"{ctx.source}:{ctx.user_id}"
        await self._ensure_session(session_id)

        message = gtypes.Content(role="user", parts=[gtypes.Part(text=ctx.message)])

        final_parts: list[str] = []
        try:
            async for event in self._runner.run_async(
                user_id=session_id,
                session_id=session_id,
                new_message=message,
            ):
                # Prefer final-response events; fall back to any text content.
                is_final = getattr(event, "is_final_response", None)
                take = is_final() if callable(is_final) else True
                if not take:
                    continue
                content = getattr(event, "content", None)
                if not content or not getattr(content, "parts", None):
                    continue
                for part in content.parts:
                    text = getattr(part, "text", None)
                    if text:
                        final_parts.append(text)
        except Exception:
            logger.exception("adk_run_failed", session_id=session_id)
            return AgentReply(text="(ADK runtime error ???撩? log)")

        return AgentReply(text="".join(final_parts).strip() or "(瘝?啣?閬?")
