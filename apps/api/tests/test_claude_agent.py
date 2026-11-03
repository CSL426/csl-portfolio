"""ClaudeAgent tests with a fake Anthropic client (no network, no API key)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import anthropic
import httpx2
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
    model: str = "claude-haiku-5-5"


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
        self.messages = _FakeMessages(replies)


def _agent(replies: list[_Response]) -> tuple[ClaudeAgent, _FakeMessages]:
    client = _FakeClient(replies)
    return ClaudeAgent(client=client), client.messages  # type: ignore[arg-type]


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
async def test_claude_sends_effort_and_no_fallbacks() -> None:
    agent, messages = _agent([_Response([_Block("thinking"), _Block("text", "你好")])])
    reply = await agent.handle(_ctx("hi"))
    assert reply.text == "你好"
    call = messages.calls[0]
    # Haiku has no server-side fallback, so these must not be sent.
    assert "fallbacks" not in call
    assert "betas" not in call
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


@pytest.mark.asyncio
async def test_claude_reset_forgets_history() -> None:
    agent, messages = _agent([_Response([_Block("text", "A")]), _Response([_Block("text", "B")])])
    await agent.handle(_ctx("one"))
    await agent.reset("test", "u1")
    await agent.handle(_ctx("two"))
    assert messages.calls[1]["messages"] == [{"role": "user", "content": "two"}]


@pytest.mark.asyncio
async def test_claude_idle_sessions_expire(monkeypatch: pytest.MonkeyPatch) -> None:
    now = [0.0]
    client = _FakeClient([_Response([_Block("text", str(i))]) for i in range(2)])
    agent = ClaudeAgent(client=client, clock=lambda: now[0])  # type: ignore[arg-type]
    monkeypatch.setattr(agent.settings, "claude_session_ttl_seconds", 60)
    await agent.handle(_ctx("one", user_id="alice"))
    now[0] = 61.0
    await agent.handle(_ctx("two", user_id="bob"))
    assert list(agent._sessions) == ["test:bob"]


@pytest.mark.asyncio
async def test_claude_session_count_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    agent, _ = _agent([_Response([_Block("text", str(i))]) for i in range(3)])
    monkeypatch.setattr(agent.settings, "claude_max_sessions", 2)
    for name in ("a", "b", "c"):
        await agent.handle(_ctx("hi", user_id=name))
    assert list(agent._sessions) == ["test:b", "test:c"]


@pytest.mark.asyncio
async def test_claude_timeout_returns_friendly_message() -> None:
    agent, messages = _agent([])

    async def _timeout(**_: Any) -> _Response:
        raise anthropic.APITimeoutError(request=httpx2.Request("POST", "https://example.test"))

    messages.create = _timeout  # type: ignore[method-assign]
    reply = await agent.handle(_ctx("hi"))
    assert "無法連線" in reply.text


def test_claude_client_bounds_the_wait_for_line(monkeypatch: pytest.MonkeyPatch) -> None:
    agent = ClaudeAgent()
    monkeypatch.setattr(agent.settings, "anthropic_api_key", "test-key")
    client = agent._ensure_client()
    assert client is not None
    assert client.timeout == 15.0
    assert client.max_retries == 1
