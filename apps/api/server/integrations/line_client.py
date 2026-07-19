from __future__ import annotations

from functools import lru_cache

from linebot.v3 import WebhookParser
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)

from server.core.config import get_settings
from server.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache
def get_parser() -> WebhookParser | None:
    settings = get_settings()
    if not settings.line_channel_secret:
        return None
    return WebhookParser(settings.line_channel_secret)


@lru_cache
def _get_configuration() -> Configuration | None:
    settings = get_settings()
    if not settings.line_channel_access_token:
        return None
    return Configuration(access_token=settings.line_channel_access_token)


def reply_text(reply_token: str, text: str) -> None:
    """Send a single text reply. No-op (with warning) if LINE not configured."""

    config = _get_configuration()
    if config is None:
        logger.warning("line_not_configured", reply_token=reply_token)
        return

    with ApiClient(config) as api_client:
        api = MessagingApi(api_client)
        api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=text)],
            )
        )
