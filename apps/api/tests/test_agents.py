import pytest
from server.agents import AgentContext, registry
from server.agents.echo import EchoAgent
from server.agents.google_adk import GoogleADKAgent


@pytest.mark.asyncio
async def test_echo_agent_echoes_message() -> None:
    agent = EchoAgent()
    reply = await agent.handle(AgentContext(user_id="u1", source="test", message="hello"))
    assert "hello" in reply.text
    assert "test" in reply.text


def test_registry_has_expected_agents() -> None:
    names = registry.names()
    assert "echo" in names
    assert "adk" in names
    assert "claude" in names


def test_registry_route_with_prefix() -> None:
    agent = registry.route("/echo ping", default="adk")
    assert agent.name == "echo"


def test_registry_route_without_prefix_uses_default() -> None:
    agent = registry.route("hi there", default="echo")
    assert agent.name == "echo"


def test_registry_strip_prefix() -> None:
    assert registry.strip_prefix("/echo hello") == "hello"
    assert registry.strip_prefix("no prefix") == "no prefix"
    assert registry.strip_prefix("/only") == ""


@pytest.mark.asyncio
async def test_adk_agent_unconfigured_returns_friendly_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When GOOGLE_API_KEY isn't set, ADK agent should degrade gracefully."""
    agent = GoogleADKAgent()
    monkeypatch.setattr(agent.settings, "google_api_key", None)
    reply = await agent.handle(AgentContext(user_id="u1", source="test", message="hi"))
    assert "GOOGLE_API_KEY" in reply.text


def test_registry_resolve_strips_prefix_even_for_default() -> None:
    agent, payload = registry.resolve("/echo hi", default="echo")
    assert agent.name == "echo"
    assert payload == "hi"


def test_registry_resolve_unknown_prefix_goes_to_default_unchanged() -> None:
    agent, payload = registry.resolve("/nope hi", default="echo")
    assert agent.name == "echo"
    assert payload == "/nope hi"
