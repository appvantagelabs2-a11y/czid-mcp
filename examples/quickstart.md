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

## 2. Free tool — no key, no payment

```bash
curl -sS -X POST https://czid.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"company_lookup","arguments":{"id":"27082440"}}}'
```

## 3. Paid tool without payment → HTTP 402

```bash
curl -sS -i -X POST https://czid.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"check_vat","arguments":{"ids":["CZ27079827"]}}}'
```

The 402 body is an [x402](https://docs.x402.org) payment schedule (network, amount, receiver).
An x402-capable client signs it and retries automatically — no account, no key.

## 4. Paid tool with a trial key

```bash
curl -sS -i -X POST https://czid.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'X-API-Key: ***' \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"check_vat","arguments":{"ids":["CZ27079827"]}}}'
```

Response header `X-Trial-Remaining: N` decrements per call. At 0 you get `402` again plus
`X-Trial-Exhausted: true`.

## 5. Health / current prices

```bash
curl -sS https://czid.casuyi.com/health
```

## 6. Modern era (spec 2026-07-28) — optional

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
