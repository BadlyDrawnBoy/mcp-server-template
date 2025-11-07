# Refactor: Turn this repository into a **generic MCP Server Skeleton**

## Goal
Produce a minimal, framework-quality **MCP server template** (Starlette / OpenAPI / SSE / Env-config / deterministic envelopes)
with **no app specialization**. Keep a clean, documented extension surface so new backends (e.g., KMyMoney via D-Bus)
can be added as plugins/adapters.

## Keep (core skeleton)
- `bridge/app.py` (factory, routing mount, OpenAPI, SSE/Readiness gates)
- `bridge/utils/*` (config/env, envelope/error helpers, safety limits)
- `.github/workflows/*` (Python CI; remove Java/Ghidra steps if any)
- `docs/` (keep structure; update content to generic MCP)
- `requirements*.txt` (trim to essentials)
- `bin/`, `.ci/`, `.githooks/` only if still relevant

## Remove (app specializations & dead code)
Delete everything that hardcodes **Ghidra** or other specific apps:
- Packages:
  - `bridge/ghidra/**`
  - `bridge/features/**` (disasm, strings, xrefs, jt, mmio, …)
  - any `bridge/api/routes/*` that import `GhidraClient` or Ghidra features
- Tests:
  - `bridge/tests/**` that target Ghidra/Disasm/Search/Xrefs/etc.
- Docs:
  - any `docs/*` with Ghidra-specific content (API, plugin ground truth, quicklinks, …)
- Scripts:
  - Ghidra/JAR/Maven/probe scripts tailored to Ghidra

## Rename / Neutralize
- API title → **"MCP Server Template API"**
- ENV prefix → **`MCP_`** (replace `GHIDRA_MCP_` / `KMYMCP_`):
  - `MCP_ENABLE_WRITES`, `MCP_MAX_WRITES_PER_REQUEST`, `MCP_MAX_ITEMS_PER_BATCH`, `MCP_AUDIT_LOG`, `MCP_URL` (if needed)
- No app names in package/module identifiers

## Provide a minimal runnable template
- Endpoints:
  - `GET /api/ping.json` → `{"ok":true,"data":{"pong":true}}`
  - `GET /api/version.json` → `{"ok":true,"data":{"version":"0.0.0"}}`
- SSE:
  - `GET /sse` with single-connection gate (second GET → 409; POST → 405)
- OpenAPI:
  - generic title/version; remove app-specific schemas
- Config:
  - env gates, deterministic envelopes, safety limits retained
- Tests:
  - minimal set for ping/version, envelope shape, SSE gate smoke
- Docs:
  - `README.md` generic (Quickstart, Config, “How to add a backend”)
  - `docs/extend.md`: guide for adding backends (adapter/routes/MCP tools)

## Acceptance Criteria (DoD)
- `uvicorn bridge.app:create_app --factory` starts without optional deps
- `GET /api/ping.json` and `/api/version.json` return `ok:true`
- `GET /sse` gate behaves as specified (409/405)
- CI green (lint + minimal tests)
- No mention of Ghidra/KMyMoney in code/docs except in the “Extend” example

## Stretch (optional)
- Simple plugin discovery (e.g., auto-mount `bridge/backends/*`)
- Example backend stub in `bridge/backends/example/` (mock only)
