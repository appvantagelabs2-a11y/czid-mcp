# czid — Czech company registry MCP server

Czech entity-registry tools for AI agents over the [Model Context Protocol](https://modelcontextprotocol.io): company lookup, VAT (DPH) status, insolvency/registry snapshot, RÚIAN address standardization, Czech identifier validation.

Data source: official **ARES REST API** (`ares.gov.cz`) — Czech open data, CC BY 4.0 (ND). No API key needed to use this service.

**Use the hosted endpoint — no install, no local process:**

```
https://czid.casuyi.com/mcp
```

MCP `2026-07-28` (2025-era clients supported too), stateless Streamable HTTP, works with Claude Code, Claude Desktop, Cursor, VS Code, and any MCP client.

## Tools

| Tool | Price | What it does |
|---|---|---|
| `company_lookup(id)` | **free** | ARES basic register: name, legal form, registered address, NACE, DIČ, data box, active registers |
| `check_vat(ids[])` | paid | RZP register: VAT payer (plátce DPH) yes/no, effective since, tax office. Batch up to 20 IČOs/DIČs |
| `entity_status(id)` | paid | KYC-style snapshot: active/cancelled, register presence (VR, RZP, insolvency RS, RCNS, SZR…), insolvency record |
| `search_company(name)` | paid | Company name search (prefix, case-insensitive) → IČOs + addresses |
| `address_check(address)` | paid | Free-text Czech address → RÚIAN-standardized (KOD ADM, PSC, city part) |
| `validate_cz(ico/dic/iban/variableSymbol)` | paid | Offline checksum validation: IČO, DIČ, IBAN, variable symbol |

`id` accepts IČO (8 digits) or DIČ (`CZ` + 10 digits).

## Connect

**Claude Code**

```bash
claude mcp add czid --transport http https://czid.casuyi.com/mcp
```

**Claude Desktop** — Settings → Connectors → *Add custom connector* → URL above.

**Cursor / VS Code (Copilot) / Windsurf / any `mcpServers` JSON client**

```json
{
  "mcpServers": {
    "czid": { "type": "http", "url": "https://czid.casuyi.com/mcp" }
  }
}
```

## Pricing — two ways to use paid tools

1. **Trial key (easiest)** — ask for a free trial key via a [GitHub issue](../../issues) or e-mail. Send it as `X-API-Key: *** header on every request; responses carry `X-Trial-Remaining: N`. When exhausted, calls fall back to x402.
2. **x402 (permissionless, no account)** — an unpaid paid-tool call returns HTTP `402` with USDC payment instructions; an x402-capable agent client signs and retries automatically. Network: `base-sepolia` today (mainnet on request). Price per call: see `GET https://czid.casuyi.com/health`.

`company_lookup` is free and never gated.

## Try it right now (curl, no client needed)

```bash
curl -sS -X POST https://czid.casuyi.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"company_lookup","arguments":{"id":"27082440"}}}'
```

→ Alza.cz a.s., Jankovcova 1522/53, Praha … (reply is one SSE `data:` line — see [examples](examples/quickstart.md)).

## Docs

- [examples/quickstart.md](examples/quickstart.md) — every call shape: list tools, free call, 402 challenge, trial key, paid x402
- [examples/clients.md](examples/clients.md) — connect from Claude Code / Desktop / Cursor / any MCP client
- [clients/python.py](clients/python.py) — minimal Python client (stdlib only)
- [clients/typescript.ts](clients/typescript.ts) — minimal TypeScript client (fetch only)

## Privacy & data

Legal-entity public data only (ARES open data). Where the register publishes a DIČ derived from a birth number (OSVČ), this service surfaces exactly what the register publishes — no additional personal data. Every response includes the source and its `datumAktualizace` per the CC BY 4.0 (ND) license. The service keeps no request logs tied to identities; trial keys are usage-counter only.

## Status / support

Open an [issue](../../issues) for: trial keys, bulk billing, mainnet x402, custom fields, uptime questions.
