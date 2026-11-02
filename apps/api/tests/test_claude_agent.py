"""ClaudeAgent tests with a fake Anthropic client (no network, no API key)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest
from server.agents import AgentContext
from server.agents.claude import ClaudeAgent


@dataclass
class _Block:
    type: str
    text: str = ""


@dataclass
class _StopDetails:
    category: str | None = None


@dataclass
class _Response:
    content: list[_Block]
    stop_reason: str = "end_turn"
    stop_details: _StopDetails | None = None
    model: str = "claude-opus-5-5"


@dataclass
class _FakeMessages:
    replies: list[_Response]
    calls: list[dict[str, Any]] = field(default_factory=list)

    async def create(self, **kwargs: Any) -> _Response:
        # Snapshot the list so later appends don't rewrite what was sent.
        self.calls.append({**kwargs, "messages": list(kwargs["messages"])})
        return self.replies.pop(0)


class _FakeClient:
    def __init__(self, replies: list[_Response]) -> None:
        self.beta = type("Beta", (), {})()
        self.beta.messages = _FakeMessages(replies)


def _agent(replies: list[_Response]) -> tuple[ClaudeAgent, _FakeMessages]:
    client = _FakeClient(replies)
    return ClaudeAgent(client=client), client.beta.messages  # type: ignore[arg-type]


def _ctx(message: str, user_id: str = "u1") -> AgentContext:
    return AgentContext(user_id=user_id, source="test", message=message)


@pytest.mark.asyncio
async def test_claude_unconfigured_returns_friendly_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agent = ClaudeAgent()
    monkeypatch.setattr(agent.settings, "anthropic_api_key", None)
    reply = await agent.handle(_ctx("hi"))
    assert "ANTHROPIC_API_KEY" in reply.text


@pytest.mark.asyncio
async def test_claude_sends_fallbacks_and_effort() -> None:
    agent, messages = _agent([_Response([_Block("thinking"), _Block("text", "你好")])])
    reply = await agent.handle(_ctx("hi"))
    assert reply.text == "你好"
    call = messages.calls[0]
    assert call["fallbacks"] == "default"
    assert call["betas"] == ["server-side-fallback-2026-07-01"]
    assert call["output_config"] == {"effort": agent.settings.claude_effort}


@pytest.mark.asyncio
async def test_claude_history_is_append_only_and_keeps_full_content() -> None:
    first = _Response([_Block("thinking"), _Block("text", "A")])
    agent, messages = _agent([first, _Response([_Block("text", "B")])])
    await agent.handle(_ctx("one"))
    await agent.handle(_ctx("two"))

    second_call = messages.calls[1]["messages"]
    assert second_call[0] == {"role": "user", "content": "one"}
    # The full content list (thinking block included) is replayed unchanged.
    assert second_call[1] == {"role": "assistant", "content": first.content}
    assert second_call[2] == {"role": "user", "content": "two"}


@pytest.mark.asyncio
async def test_claude_sessions_are_isolated() -> None:
    agent, messages = _agent([_Response([_Block("text", "A")]), _Response([_Block("text", "B")])])
    await agent.handle(_ctx("hi", user_id="alice"))
    await agent.handle(_ctx("hi", user_id="bob"))
    assert len(messages.calls[1]["messages"]) == 1


@pytest.mark.asyncio
async def test_claude_refusal_is_not_stored() -> None:
    refused = _Response([], stop_reason="refusal", stop_details=_StopDetails("cyber"))
    agent, messages = _agent([refused, _Response([_Block("text", "ok")])])
    reply = await agent.handle(_ctx("bad"))
    assert "沒辦法回答" in reply.text
    await agent.handle(_ctx("good"))
    assert messages.calls[1]["messages"] == [{"role": "user", "content": "good"}]


@pytest.mark.asyncio
async def test_claude_starts_over_after_max_turns(monkeypatch: pytest.MonkeyPatch) -> None:
    agent, messages = _agent([_Response([_Block("text", str(i))]) for i in range(3)])
    monkeypatch.setattr(agent.settings, "claude_max_turns", 1)
    await agent.handle(_ctx("one"))
    await agent.handle(_ctx("two"))
    assert messages.calls[1]["messages"] == [{"role": "user", "content": "two"}]
