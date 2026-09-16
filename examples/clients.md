# Connecting from MCP clients

The hosted server is a remote Streamable-HTTP MCP endpoint — no install, no local process,
no API key, all tools free.

## Claude Code

```bash
claude mcp add czid --transport http https://czid.casuyi.com/mcp
```

Verify: `claude mcp list` → `czid: ... ✔ connected`. Inside a session, `/mcp` shows the 6 tools.

## Claude Desktop

Settings → Connectors → **Add custom connector** → URL `https://czid.casuyi.com/mcp`.

## Cursor / VS Code (Copilot) / Windsurf / any `mcpServers` JSON client

```json
{
  "mcpServers": {
    "czid": {
      "type": "http",
      "url": "https://czid.casuyi.com/mcp"
    }
  }
}
```

## Python

See [`../clients/`](../clients/) — zero-dependency clients (stdlib `urllib` / native `fetch`).
