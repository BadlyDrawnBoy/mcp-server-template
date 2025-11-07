"""HTTP and MCP API surfaces for the MCP server template."""

from .routes import make_routes
from .tools import register_tools

__all__ = ["make_routes", "register_tools"]
