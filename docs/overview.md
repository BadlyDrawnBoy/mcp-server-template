# Overview

The MCP Server Template provides a backend-neutral starting point for building Model Context Protocol servers. It focuses on
essential infrastructure—SSE transport, deterministic envelopes, environment-aware safety limits—and leaves backend-specific logic
to dedicated adapters.

Key components:

- `bridge/app.py`: assembles the Starlette application, SSE transport, and OpenAPI schema
- `bridge/api/`: HTTP routes and envelope helpers
- `bridge/utils/`: reusable logging, configuration, and error utilities
- `bridge/backends/`: pluggable tool providers discovered at runtime

Use this template when you need a predictable, testable skeleton before wiring in a real backend.
