from typing import Any

from fastapi import APIRouter, HTTPException, status

from server.agents import AgentContext, registry
from server.core.config import get_settings
from server.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    settings = get_settings()
    agent_name = req.agent or settings.default_agent
    agent = registry.get(agent_name)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown agent: {agent_name}. Available: {registry.names()}",
        )

    ctx = AgentContext(user_id=req.user_id, source="web", message=req.message)
    reply = await agent.handle(ctx)
    return ChatResponse(agent=agent.name, text=reply.text, extra=reply.extra)


@router.get("/agents")
async def list_agents() -> dict[str, Any]:
    return {"agents": registry.names(), "default": get_settings().default_agent}
