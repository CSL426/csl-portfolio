from server.agents.base import BaseAgent
from server.agents.claude import ClaudeAgent
from server.agents.echo import EchoAgent
from server.agents.google_adk import GoogleADKAgent


class AgentRegistry:
    """In-memory registry of named agents. Add storage later if needed."""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._aliases: dict[str, str] = {}

    def register(self, agent: BaseAgent, aliases: tuple[str, ...] = ()) -> None:
        self._agents[agent.name] = agent
        for alias in aliases:
            self._aliases[alias] = agent.name

    def get(self, name: str) -> BaseAgent | None:
        return self._agents.get(self._aliases.get(name, name))

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

    def resolve(self, message: str, default: str) -> tuple[BaseAgent, str]:
        """Pick the agent for a raw message and return it with the payload.

        A leading `/<name>` naming a registered agent selects it and is removed
        from the payload, even when it names the default agent. Anything else
        goes to the default agent unchanged.
        """
        prefix = self._parse_prefix(message)
        agent = self.get(prefix) if prefix else None
        if agent is not None:
            return agent, self.strip_prefix(message)
        return self.get(default) or self._agents[default], message

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
# `/adk` was the old command; keep it working for anyone who learned it.
registry.register(GoogleADKAgent(), aliases=("adk",))
registry.register(ClaudeAgent())
