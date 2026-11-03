from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Final, Literal

EMPTY_MESSAGE_REPLY: Final = "（請在指令後面輸入訊息）"


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

    async def reset(self, source: str, user_id: str) -> None:  # noqa: B027
        """Forget a user's conversation. Stateless agents have nothing to do."""
