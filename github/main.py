#!/usr/bin/env python3
"""GitHub repository search plugin for QsFlow."""

import json
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

# Workspace root, home of the shared qsflow_plugin package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from qsflow_plugin import Item, plugin

ICON = "papirus:github"


@plugin.search(
    id="github",
    name="GitHub",
    icon=ICON,
    description="Search GitHub repositories",
)
def search(text: str) -> list[Item]:
    query = urlencode({"q": text, "per_page": 8})
    # A stalled api.github.com must fail fast and visibly: the core gives a host
    # 5s and then kills it (the row would just be empty), while this raises
    # inside the plugin and the framework shows "Search failed: timed out".
    with urlopen(
        f"https://api.github.com/search/repositories?{query}", timeout=4
    ) as response:
        data = json.load(response)
    return [
        Item(
            title=repo["full_name"],
            summary=repo.get("description"),
            on_click=repo["html_url"],
            icon=ICON,
            # a repo hit is a one-shot search result, not a target to re-open
            ephemeral=True,
        )
        for repo in data["items"]
    ]


plugin.run()
