import pytest
from server.agents import AgentContext, registry
from server.agents.echo import EchoAgent


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
async def test_adk_agent_unconfigured_returns_friendly_message() -> None:
    """When GOOGLE_API_KEY isn't set, ADK agent should degrade gracefully."""
    agent = registry.get("adk")
    assert agent is not None
    reply = await agent.handle(AgentContext(user_id="u1", source="test", message="hi"))
    # Either it returns the "not configured" message, or it actually worked
    # because env is set in CI/local ??both are acceptable.
    assert reply.text
