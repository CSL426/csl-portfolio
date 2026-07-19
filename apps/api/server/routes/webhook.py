from __future__ import annotations

from typing import Any

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request, status
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from server.agents import AgentContext, registry
from server.core.config import get_settings
from server.core.logging import get_logger
from server.integrations.line_client import get_parser, reply_text

router = APIRouter(prefix="/webhook", tags=["webhook"])
logger = get_logger(__name__)


@router.post("/line", status_code=status.HTTP_200_OK)
async def line_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str = Header(default=""),
) -> dict[str, int]:
    """LINE Messaging API webhook.

    LINE retries on non-2xx, so we always 200 and process events in the background.
    Signature verification still rejects clearly forged requests with 400.
    """

    parser = get_parser()
    if parser is None:
        logger.error("line_webhook_unconfigured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LINE channel secret not configured",
        )

    body_bytes = await request.body()
    body_text = body_bytes.decode("utf-8")

    try:
        events = parser.parse(body_text, x_line_signature)
    except InvalidSignatureError as e:
        logger.warning("line_signature_invalid")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature"
        ) from e

    for event in events:
        background_tasks.add_task(_dispatch_event, event)

    return {"received": len(events)}


async def _dispatch_event(event: Any) -> None:
    try:
        if not isinstance(event, MessageEvent):
            logger.info("line_event_ignored", type=type(event).__name__)
            return
        if not isinstance(event.message, TextMessageContent):
            logger.info("line_message_unsupported", type=type(event.message).__name__)
            return

        settings = get_settings()
        raw = event.message.text
        agent = registry.route(raw, default=settings.default_agent)
        payload = registry.strip_prefix(raw) if agent.name != settings.default_agent else raw

        user_id = (event.source.user_id if event.source else None) or "unknown"

        ctx = AgentContext(
            user_id=user_id,
            source="line",
            message=payload,
            metadata={"reply_token": event.reply_token},
        )
        reply = await agent.handle(ctx)
        reply_text(event.reply_token, reply.text)

        logger.info("line_event_handled", agent=agent.name, user_id=user_id)
    except Exception:
        logger.exception("line_event_dispatch_failed")
