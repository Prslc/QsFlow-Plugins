"""Result rows and the helpers that build their ``on_click`` values."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class Item:
    """One search-result row.

    ``title`` is required; the rest default to "not set". The four protocol
    keys are always emitted on the wire, with ``ephemeral`` only when set.
    An unset ``icon`` falls back to the plugin icon.

    ``ephemeral=True`` asks the core not to record this row in usage history,
    for a one-shot hit whose target is not worth re-opening later.
    """

    title: str
    summary: str | None = None
    on_click: str | None = None
    icon: str | None = None
    ephemeral: bool = False

    def as_dict(self, default_icon: str | None = None) -> dict[str, Any]:
        """The wire form for this row, with the plugin icon as fallback."""
        item: dict[str, Any] = {
            "title": self.title,
            "summary": self.summary,
            "on_click": self.on_click,
            "icon": self.icon if self.icon is not None else default_icon,
        }
        if self.ephemeral:
            item["ephemeral"] = True
        return item


def copy_text(text: str) -> str:
    """An ``on_click`` that writes ``text`` to the Wayland clipboard."""
    return "copy:" + json.dumps({"text": text}, ensure_ascii=False)


def hint(title: str, detail: str | None = None) -> Item:
    """A display-only row for usage or argument-error guidance."""
    return Item(title=title, summary=detail)


def split_command(text: str) -> tuple[str, str]:
    """Split ``"verb rest"`` into ``(verb, rest)``.

    The verb is lowercased for case-insensitive routing; the payload keeps
    its internal whitespace and is stripped at the edges. A bare verb yields
    an empty payload.
    """
    parts = text.split(maxsplit=1)
    verb = parts[0].lower() if parts else ""
    payload = parts[1].strip() if len(parts) > 1 else ""
    return verb, payload
