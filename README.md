# MCP Server Template

A lightweight, backend-neutral skeleton for building Model Context Protocol (MCP) servers. The template focuses on the plumbing
that every server needs – deterministic envelopes, Starlette routing, Server-Sent Events (SSE) with readiness gates, and a clean
extension surface for registering tools.

## Features

- Minimal HTTP API with deterministic `{ok,data,errors}` envelopes
- Guarded SSE endpoint that enforces a single active connection and readiness checks
- FastMCP integration ready for stdio or SSE transports
- Environment-driven safety limits (`MCP_MAX_*`) and audit logging toggle
- Pluggable backend discovery (`bridge/backends`) for registering custom tools

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn bridge.app:create_app --factory --host 127.0.0.1 --port 8000
```

Once the server is running:

```bash
curl -s http://127.0.0.1:8000/api/ping.json | jq
curl -s http://127.0.0.1:8000/api/version.json | jq
```

## Configuration

Runtime behaviour is controlled via environment variables with the `MCP_` prefix:

- `MCP_ENABLE_WRITES` – enable write-capable tools (default: `false`)
- `MCP_MAX_WRITES_PER_REQUEST` – maximum writes allowed in a single request (default: `2`)
- `MCP_MAX_ITEMS_PER_BATCH` – maximum batch size enforced by `enforce_batch_limit` (default: `256`)
- `MCP_AUDIT_LOG` – optional path to a JSONL audit log file

An `.env.sample` file is provided as a reference.

## HTTP Endpoints

| Route | Description |
|-------|-------------|
| `GET /api/ping.json` | Health check returning `{"pong": true}` |
| `GET /api/version.json` | Template semantic version (default `0.0.0`) |
| `GET /api/state` | Diagnostics about SSE readiness and active connections |
| `GET /api/openapi.json` | Generated OpenAPI document for the registered routes |

The `/sse` endpoint exposes the MCP SSE transport with a single-connection gate. The `/messages` mount provides the FastMCP
message transport and obeys the same readiness rules.

## Extending the server

Drop backend modules into `bridge/backends/` and implement a `register(server: FastMCP)` function. Modules are discovered
automatically during startup and receive the shared `FastMCP` instance for registering tools.

An illustrative stub is included in `bridge/backends/example.py`.

## Development

Run the tests with:

```bash
pytest
```

To experiment with the SSE transport, start the server and connect twice:

```bash
curl -iN http://127.0.0.1:8000/sse
curl -i http://127.0.0.1:8000/sse   # returns HTTP 409 while the first stream is active
```

## License

This project is distributed under the terms of the MIT License. See [LICENSE](LICENSE) for details.
