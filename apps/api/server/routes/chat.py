from typing import Any

from fastapi import APIRouter, HTTPException, status

from server.agents import AgentContext, registry
from server.core.config import get_settings
from server.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    settings = get_settings()
    message = req.message
    if req.agent:
        agent = registry.get(req.agent)
        if agent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unknown agent: {req.agent}. Available: {registry.names()}",
            )
    else:
        # Same convention as the LINE webhook: a leading `/<agent>` picks the agent.
        agent, message = registry.resolve(message, default=settings.default_agent)

    if not message.strip():
        return ChatResponse(agent=agent.name, text="（請在指令後面輸入訊息）")

    ctx = AgentContext(user_id=req.user_id, source="web", message=message)
    reply = await agent.handle(ctx)
    return ChatResponse(agent=agent.name, text=reply.text, extra=reply.extra)


@router.get("/agents")
async def list_agents() -> dict[str, Any]:
    return {"agents": registry.names(), "default": get_settings().default_agent}
