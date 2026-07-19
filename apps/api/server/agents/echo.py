from server.agents.base import AgentContext, AgentReply, BaseAgent


class EchoAgent(BaseAgent):
    """Echo agent ??verifies the pipeline end-to-end without LLM dependencies."""

    name = "echo"

    async def handle(self, ctx: AgentContext) -> AgentReply:
        return AgentReply(text=f"[echo:{ctx.source}] {ctx.message}")
