"""Example backend illustrating the expected extension surface."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register(server: FastMCP) -> None:
    """Register demonstration tools on the provided ``server``.

    The example intentionally avoids touching real systems. It exposes a single
    ``echo"` tool that simply returns the supplied text.
    """

    @server.tool()
    async def echo(message: str) -> str:  # pragma: no cover - illustrative only
        return message


__all__ = ["register"]
