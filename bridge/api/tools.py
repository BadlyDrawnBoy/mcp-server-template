"""Tool registration plumbing for the MCP server template."""
from __future__ import annotations

import importlib
import logging
from importlib import util as importlib_util
from pkgutil import iter_modules

from mcp.server.fastmcp import FastMCP

_LOGGER = logging.getLogger("bridge.api.tools")


def _iter_backend_modules() -> list[str]:
    """Yield backend module names within ``bridge.backends`` if present."""

    package_name = "bridge.backends"
    spec = importlib_util.find_spec(package_name)
    if spec is None or spec.submodule_search_locations is None:
        return []

    modules: list[str] = []
    for _, name, _ in iter_modules(spec.submodule_search_locations, f"{package_name}."):
        modules.append(name)
    return modules


def register_tools(server: FastMCP) -> list[str]:
    """Register any builtin or discovered tool providers with ``server``.

    The template ships without first-party tools. Instead, it discovers modules
    under :mod:`bridge.backends` and calls their ``register(server)`` function if
    available. Custom deployments can drop lightweight adapters into that package
    or distribute them as installable Python modules.
    """

    loaded: list[str] = []
    for module_name in _iter_backend_modules():
        try:
            module = importlib.import_module(module_name)
        except Exception:  # pragma: no cover - defensive guard
            _LOGGER.exception("backend.import_error", extra={"module": module_name})
            continue

        register = getattr(module, "register", None)
        if callable(register):
            register(server)
            loaded.append(module_name)
        else:
            _LOGGER.debug("backend.missing_register", extra={"module": module_name})
    return loaded


__all__ = ["register_tools"]
