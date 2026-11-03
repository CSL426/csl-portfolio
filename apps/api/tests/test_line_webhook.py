from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from server.agents import EMPTY_MESSAGE_REPLY, registry
from server.routes import webhook


def _event(text: str) -> MagicMock:
    event = MagicMock(spec=MessageEvent)
    event.message = MagicMock(spec=TextMessageContent, text=text)
    event.reply_token = "token"
    event.source = MagicMock(user_id="U1")
    return event


@pytest.mark.asyncio
async def test_bare_prefix_asks_for_a_message_without_calling_the_agent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    replies: list[tuple[str, str]] = []
    monkeypatch.setattr(webhook, "reply_text", lambda token, text: replies.append((token, text)))
    agent = registry.get("echo")
    assert agent is not None
    handle = MagicMock()
    monkeypatch.setattr(agent, "handle", handle)

    await webhook._dispatch_event(_event("/echo"))

    assert replies == [("token", EMPTY_MESSAGE_REPLY)]
    handle.assert_not_called()
