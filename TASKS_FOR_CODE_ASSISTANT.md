# Refactor: Turn this repository into a **generic MCP Server Skeleton**

## Goal
Produce a minimal, framework-quality **MCP server template** (Starlette/OpenAPI/SSE/Env-config/Deterministic envelopes)
with **no app specialization**. Keep a clean, documented extension surface so new backends (e.g., KMyMoney via D-Bus)
can be added as plugins/adapters.

## Keep (core skeleton)
- `bridge/app.py` (factory, routing mount, OpenAPI, SSE/Readiness gates).
- `bridge/utils/*` (config/env, envelope/error helpers, safety limits).
- `.github/workflows/*` (Python CI; remove Java/Ghidra steps if any).
- `docs/` (keep structure; update content to generic MCP).
- `requirements*.txt` (trim to essentials).
- `bin/`, `.ci/`, `.githooks/` only if still relevant.

## Remove (app specializations & dead code)
Delete everything that hardcodes **Ghidra** or other specific apps:

- Packages:
  - `bridge/ghidra/**`
  - `bridge/features/**` (disasm, strings, xrefs, jt, mmio, …)
  - alle `bridge/api/routes/*` die `GhidraClient` oder Ghidra-Features importieren
- Tests:
  - `bridge/tests/**` die sich auf Ghidra/Disasm/Search/Xrefs/etc. beziehen
- Docs:
  - `docs/*` mit Ghidra-Inhalten (API, plugin ground truth, ghidra quicklinks, …)
- Scripts:
  - alles, was Ghidra/JAR/Maven/Probe/SSE-Smoke explizit für Ghidra verwendet

> Tipp: nutze globs und sichere dich mit Grep ab (`git grep -n 'Ghidra'`).

## Rename / Neutralize
- API title: **"MCP Server Template API"**.
- ENV Prefix: **`MCP_`** (ersetze `GHIDRA_MCP_` / `KMYMCP_` → `MCP_`).
  - `MCP_ENABLE_WRITES`, `MCP_MAX_WRITES_PER_REQUEST`, `MCP_MAX_ITEMS_PER_BATCH`, `MCP_AUDIT_LOG`, `MCP_URL` (falls benötigt).
- Package hints: keine App-Begriffe in Modulnamen.

## Provide a minimal runnable template
- Endpoints:
  - `GET /api/ping.json` → `{ok:true,"data":{"pong":true}}`
  - `GET /api/version.json` → `{ok:true,"data":{"version":"0.0.0"}}`
- SSE:
  - `GET /sse` mit Einbahn-Policy (1 aktive Verbindung), 409/405 wie bisher.
- OpenAPI:
  - aktualisiere Titel/Version; ersetze App-spezifische Schemas.
- Config:
  - env-gates, deterministic envelopes, safety-limits bleiben erhalten.
- Tests:
  - 2–3 minimalistische Tests (ping/version, envelope shape, SSE gate smoke).
- Docs:
  - `README.md` kurz & generisch (Quickstart, Config, “How to add a backend”).
  - `docs/extend.md`: Anleitung für neue Backends (Adapter/Routes/MCP-Tools).

## Acceptance Criteria (DoD)
- `uvicorn bridge.app:create_app --factory` startet ohne optionalen Abhängigkeiten.
- `curl /api/ping.json` und `/api/version.json` liefern `ok:true`.
- `GET /sse` Gate funktioniert (409/405 korrekt).
- CI grün (Lint + Unit/Contract minimal).
- Keine Erwähnung von Ghidra/KMyMoney in Code/Docs außer im "Extend"-Beispiel.

## Stretch (optional)
- Plugin-discovery (z. B. `bridge/backends/*` auto-mount).
- Example backend stub in `bridge/backends/example/` (nur Mock).

