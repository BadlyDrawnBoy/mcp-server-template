"""Backend discovery helpers for the MCP server template."""
from __future__ import annotations

from importlib import import_module, util as importlib_util
from pkgutil import iter_modules
from typing import Iterable

from mcp.server.fastmcp import FastMCP


def _iter_backend_modules() -> Iterable[str]:
    package_name = __name__
    spec = importlib_util.find_spec(package_name)
    if spec is None or spec.submodule_search_locations is None:
        return []
    return tuple(
        name for _, name, _ in iter_modules(spec.submodule_search_locations, f"{package_name}.")
    )


def register_all(server: FastMCP) -> list[str]:
    """Import each backend module and invoke its ``register`` hook."""

    loaded: list[str] = []
    for module_name in _iter_backend_modules():
        module = import_module(module_name)
        hook = getattr(module, "register", None)
        if callable(hook):
            hook(server)
            loaded.append(module_name)
    return loaded


def available_backends() -> tuple[str, ...]:
    """Return the discoverable backend module names."""

    return tuple(_iter_backend_modules())


__all__ = ["available_backends", "register_all"]
