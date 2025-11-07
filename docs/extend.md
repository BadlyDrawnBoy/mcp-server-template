# Extending the Template

Backends contribute MCP tools by providing modules under `bridge/backends/`. Each module should expose a
`register(server: FastMCP) -> None` function that uses the FastMCP decorator API to declare tools, prompts, or resources.

```python
# bridge/backends/my_backend.py
from mcp.server.fastmcp import FastMCP


def register(server: FastMCP) -> None:
    @server.tool()
    async def whoami() -> dict[str, str]:
        return {"name": "template", "status": "ok"}
```

Modules are discovered automatically when `bridge.app.configure()` runs. If a module fails to import or lacks a `register`
function it is skipped with a debug log message, allowing you to iterate rapidly.

For more advanced scenarios, consider distributing your backend as an installable package that exposes a namespace package at
`bridge.backends`. The discovery mechanism uses `pkgutil.iter_modules` and therefore respects namespace packages by default.
