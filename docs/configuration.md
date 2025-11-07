# Configuration

The server reads environment variables with the `MCP_` prefix during startup. These controls are centralised in
`bridge/utils/config.py`.

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_ENABLE_WRITES` | `false` | Allows tool implementations to perform write operations when true. |
| `MCP_MAX_WRITES_PER_REQUEST` | `2` | Upper bound enforced by `record_write_attempt`. |
| `MCP_MAX_ITEMS_PER_BATCH` | `256` | Maximum allowed batch size tracked by `enforce_batch_limit`. |
| `MCP_AUDIT_LOG` | _(unset)_ | Optional filesystem path for audit logging (JSON lines). |

Set these via environment variables, an `.env` file, or your process manager.
