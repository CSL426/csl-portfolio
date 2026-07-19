from server.agents.base import BaseAgent
from server.agents.echo import EchoAgent
from server.agents.google_adk import GoogleADKAgent


class AgentRegistry:
    """In-memory registry of named agents. Add storage later if needed."""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> BaseAgent | None:
        return self._agents.get(name)

    def names(self) -> list[str]:
        return sorted(self._agents.keys())

    def route(self, message: str, default: str) -> BaseAgent:
        """Pick an agent for a raw user message.

        Convention: a leading `/<name>` selects that agent; otherwise default.
        Examples:
          "/echo hello"   -> echo agent, message "hello"
          "hi"            -> default agent, message "hi"
        """
        agent = self.get(self._parse_prefix(message) or default) or self._agents[default]
        return agent

    @staticmethod
    def _parse_prefix(message: str) -> str | None:
        stripped = message.strip()
        if not stripped.startswith("/"):
            return None
        head = stripped.split(maxsplit=1)[0]
        return head[1:] or None

    @staticmethod
    def strip_prefix(message: str) -> str:
        stripped = message.strip()
        if not stripped.startswith("/"):
            return message
        parts = stripped.split(maxsplit=1)
        return parts[1] if len(parts) > 1 else ""


registry = AgentRegistry()
registry.register(EchoAgent())
registry.register(GoogleADKAgent())
