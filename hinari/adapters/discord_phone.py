"""Discord phone: the only module importing discord.py.

Owns the in-memory room buffer. on_message only appends plus sets flags;
it never calls the LLM. The TRIGGER loop in main.py is the only waker.
"""

from __future__ import annotations

import asyncio
import logging

log = logging.getLogger("hinari.phone")


class Phone:
    """In-memory mirror of the single allowed channel."""

    def __init__(self) -> None:
        self.messages: list[dict] = []  # [{id,from,from_id,time,text,mention}]
        # ponytail: unbounded buffer; cap it when channel volume demands.

    def note_message(
        self,
        msg_id: int,
        author: str,
        author_id: int,
        created_min: int,
        text: str,
        mention: bool,
        reply_to: int | None = None,
        quoted: str | None = None,
    ) -> None:
        self.messages.append(
            {
                "id": msg_id,
                "from": author,
                "from_id": author_id,
                "time": created_min,
                "text": text,
                "mention": mention,
                "reply_to": reply_to,
                "quoted": quoted,
            }
        )

    def backfill(self, fetched: list[dict]) -> None:
        """Merge older fetched bubbles, keeping time order, no duplicates."""
        seen = {m["id"] for m in self.messages}
        for m in fetched:
            if m["id"] not in seen:
                self.messages.append(m)
                seen.add(m["id"])
        self.messages.sort(key=lambda m: (m["time"], m["id"]))


async def send_bubbles(channel, items: list[dict]) -> list[int]:
    """Send each bubble (replying where asked) with typing. Returns sent ids."""
    import discord as _discord

    sent: list[int] = []
    for item in items:
        bubble = item["text"]
        # ponytail: linear typing delay; exact curve deferred per LLD section 10.
        delay = min(len(bubble) * 0.02, 5.0)
        try:
            async with channel.typing():
                await asyncio.sleep(delay)
                if item.get("reply_to"):
                    ref = _discord.MessageReference(
                        message_id=item["reply_to"], channel_id=channel.id,
                        fail_if_not_exists=False)
                    msg = await channel.send(bubble, reference=ref)
                else:
                    msg = await channel.send(bubble)
            sent.append(msg.id)
        except Exception as exc:  # keep the tool loop alive; main logs it
            log.warning("send failed: %s", type(exc).__name__)
            break
    return sent
