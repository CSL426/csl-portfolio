from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class AgentContext:
    """Context handed to an Agent.

    `source` lets agents adapt response shape (e.g. shorter for LINE).
    `user_id` is platform-scoped; pair with `source` for uniqueness.
    """

    user_id: str
    source: Literal["line", "web", "test"]
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentReply:
    text: str
    # Optional structured payload — e.g. quick-reply buttons, images, citations.
    extra: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """All AI agents implement this interface.

    Implementations should be stateless w.r.t. instance attributes —
    persist state via metadata or an external store keyed on (source, user_id).
    """

    name: str

    @abstractmethod
    async def handle(self, ctx: AgentContext) -> AgentReply:
        """Process a single user turn and return one reply."""
