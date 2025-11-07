# Getting Started

## 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

## 2. Run the server

```bash
uvicorn bridge.app:create_app --factory --host 127.0.0.1 --port 8000
```

The server exposes:

- `GET /api/ping.json`
- `GET /api/version.json`
- `GET /api/state`
- `GET /api/openapi.json`
- `GET /sse`
- `POST /messages`

## 3. Connect an MCP client

The template bundles an OpenWebUI-compatible shim. Use the CLI helpers or the FastMCP client to point your tooling at the `/sse`
endpoint. Only one SSE client can be active at a time; additional connections return HTTP 409 until the first disconnects.

## 4. Extend with tools

Create a module under `bridge/backends/` with a `register(server)` function. Register tools using the FastMCP decorator API. The
example backend `bridge/backends/example.py` demonstrates a simple `echo` tool.
