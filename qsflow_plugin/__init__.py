"""Public API for building a QsFlow external plugin host.

A plugin is one ``main.py`` that registers its handlers and then calls
``plugin.run()``:

    from qsflow_plugin import plugin, Item, copy_text

    @plugin.search(id="example", name="Example", keyword="ex",
                   icon="papirus:star", description="Demo plugin")
    def search(text: str) -> list[Item]:
        return [Item(title="Hello", on_click=copy_text(text))]

    plugin.run()

``plugin.run()`` serves the stdin/stdout JSON-RPC 2.0 loop. The wire protocol
is documented in the QsFlow repository (``docs/en/jsonrpc.md``).
"""

from ._item import Item, copy_text, hint, split_command
from ._plugin import Plugin
from ._server import Server, serve

plugin = Plugin()

__version__ = "0.1.0"

__all__ = [
    "plugin",
    "Item",
    "copy_text",
    "hint",
    "split_command",
    "Plugin",
    "Server",
    "serve",
]
