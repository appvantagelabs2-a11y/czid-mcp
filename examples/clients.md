# Connecting from MCP clients

The hosted server is a remote Streamable-HTTP MCP endpoint — no install, no local process,
no API key for free tools.

## Claude Code

```bash
claude mcp add czid --transport http https://czid.casuyi.com/mcp
```

With a trial key (extra header, forwarded on every request):

```bash
claude mcp add czid --transport http https://czid.casuyi.com/mcp \
  --header "X-API-Key: ***"
```

Verify: `claude mcp list` → `czid: ... ✔ connected`. Inside a session, `/mcp` shows the 6 tools.

## Claude Desktop

Settings → Connectors → **Add custom connector** → URL `https://czid.casuyi.com/mcp`.
(Desktop cannot send custom headers — use x402 for paid tools there.)

## Cursor / VS Code (Copilot) / Windsurf / any `mcpServers` JSON client

```json
{
  "mcpServers": {
    "czid": {
      "type": "http",
      "url": "https://czid.casuyi.com/mcp",
      "headers": { "X-API-Key": "<your-trial-key>" }
    }
  }
}
```

Drop `headers` if you only use the free `company_lookup` tool or pay via x402.

## Python / TypeScript

See [`../clients/`](../clients/) — zero-dependency clients (stdlib `urllib` / native `fetch`),
including trial-key and SSE handling.
