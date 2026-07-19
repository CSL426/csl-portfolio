from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    user_id: str = Field(default="anonymous", max_length=128)
    agent: str | None = Field(default=None, description="Override agent name")


class ChatResponse(BaseModel):
    agent: str
    text: str
    extra: dict[str, Any] = Field(default_factory=dict)


class AgentInfo(BaseModel):
    name: str
