# Quickstart — raw JSON-RPC

Protocol: MCP `2026-07-28` (2025-era clients also work unchanged). Every request is a
`POST /mcp` with both headers:

```
Content-Type: application/json
Accept: application/json, text/event-stream
```

The reply is one SSE event: `event: message` + `data: {json}` — parse the line after `data: `.
(Prefer ready-made clients: [../clients/python.py](../clients/python.py) does all of this.)

## 1. List tools

```bash
curl -sS -X POST https://czid.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## 2. Call a tool

```bash
curl -sS -X POST https://czid.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"company_lookup","arguments":{"id":"27082440"}}}'
```

## 3. Any tool — same call shape

```bash
curl -sS -X POST https://czid.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"check_vat","arguments":{"ids":["CZ27079827"]}}}'
```

## 4. Health

```bash
curl -sS https://czid.casuyi.com/health
```

## 5. Modern era (spec 2026-07-28) — optional

The server also accepts header-routed requests with the per-request envelope. A v2 SDK client
(`@modelcontextprotocol/client@2`, `versionNegotiation: "auto"`) negotiates it automatically:

```bash
curl -sS -X POST https://czid.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: server/discover' \
  -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientInfo":{"name":"curl","version":"1"},"io.modelcontextprotocol/clientCapabilities":{}}}}'
```
