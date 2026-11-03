"""Web visitors are isolated by a server-issued cookie and rate limited."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from server.agents import AgentContext, AgentReply, BaseAgent, registry
from server.core.config import get_settings
from server.main import app
from server.routes.chat import SESSION_COOKIE


class _RecordingAgent(BaseAgent):
    name = "recording"

    def __init__(self) -> None:
        self.user_ids: list[str] = []
        self.resets: list[tuple[str, str]] = []

    async def handle(self, ctx: AgentContext) -> AgentReply:
        self.user_ids.append(ctx.user_id)
        return AgentReply(text="ok")

    async def reset(self, source: str, user_id: str) -> None:
        self.resets.append((source, user_id))


@pytest.fixture
def agent(monkeypatch: pytest.MonkeyPatch) -> _RecordingAgent:
    recording = _RecordingAgent()
    monkeypatch.setitem(registry._agents, recording.name, recording)
    return recording


def _send(client: TestClient, **body: str) -> int:
    payload = {"message": "hi", "agent": "recording", **body}
    return client.post("/api/chat", json=payload).status_code


def test_visitors_get_separate_sessions_even_with_the_same_user_id(
    agent: _RecordingAgent,
) -> None:
    # A client-supplied user_id used to decide whose history was loaded.
    _send(TestClient(app), user_id="web-user")
    _send(TestClient(app), user_id="web-user")
    assert agent.user_ids[0] != agent.user_ids[1]


def test_cookie_keeps_a_visitor_on_one_session(agent: _RecordingAgent) -> None:
    client = TestClient(app)
    _send(client)
    _send(client)
    assert agent.user_ids[0] == agent.user_ids[1]


def test_cookie_is_http_only_and_secure_behind_https() -> None:
    r = TestClient(app).post(
        "/api/chat",
        json={"message": "hi", "agent": "echo"},
        headers={"x-forwarded-proto": "https"},
    )
    cookie = r.headers["set-cookie"].lower()
    assert "httponly" in cookie
    assert "secure" in cookie
    assert "samesite=lax" in cookie


def test_malformed_cookie_is_replaced(agent: _RecordingAgent) -> None:
    client = TestClient(app, cookies={SESSION_COOKIE: "attacker-chosen"})
    r = client.post("/api/chat", json={"message": "hi", "agent": "recording"})
    assert SESSION_COOKIE in r.headers["set-cookie"]


def test_reset_clears_the_session_in_every_agent(agent: _RecordingAgent) -> None:
    client = TestClient(app)
    _send(client)
    assert client.delete("/api/chat/session").status_code == 204
    assert agent.resets == [("web", agent.user_ids[0])]


def test_reset_without_a_session_is_a_no_op(agent: _RecordingAgent) -> None:
    assert TestClient(app).delete("/api/chat/session").status_code == 204
    assert agent.resets == []


def test_session_limit_returns_429(agent: _RecordingAgent, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(get_settings(), "chat_limit_per_session_per_minute", 2)
    client = TestClient(app)
    assert [_send(client) for _ in range(3)] == [200, 200, 429]
    assert len(agent.user_ids) == 2


def test_ip_limit_ignores_spoofed_forwarded_entries(
    agent: _RecordingAgent, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(get_settings(), "chat_limit_per_ip_per_minute", 2)
    codes = [
        TestClient(app)
        .post(
            "/api/chat",
            json={"message": "hi", "agent": "recording"},
            headers={"x-forwarded-for": f"10.0.0.{i}, 203.0.113.7"},
        )
        .status_code
        for i in range(3)
    ]
    assert codes == [200, 200, 429]


def test_daily_cap_is_shared_by_all_visitors(
    agent: _RecordingAgent, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(get_settings(), "chat_limit_per_day", 1)
    assert _send(TestClient(app)) == 200
    assert _send(TestClient(app)) == 429


def test_empty_message_does_not_use_up_the_limit(
    agent: _RecordingAgent, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(get_settings(), "chat_limit_per_day", 1)
    client = TestClient(app)
    assert client.post("/api/chat", json={"message": "/echo"}).status_code == 200
    assert _send(client) == 200
