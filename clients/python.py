#!/usr/bin/env python3
"""Minimal czid-mcp client — stdlib only (no MCP SDK needed for a stateless server).

Usage:
  python3 python.py company_lookup id=27082440
  python3 python.py check_vat ids=CZ27079827,CZ27105090
  CZID_API_KEY=*** python3 python.py check_vat ids=CZ27079827

Paid tools return 402 unless you pay via x402 (needs an x402-capable client)
or send a trial key (CZID_API_KEY env or --key).
"""
import json
import os
import sys
import urllib.error
import urllib.request

URL = os.environ.get("CZID_URL", "https://czid.casuyi.com/mcp")


def rpc(method, params=None, api_key=None, req_id=1):
    body = json.dumps(
        {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}}
    ).encode()
    headers = {
        "Content-Type": "application/json",
            "User-Agent": "mcp-example-client/1.0",
        "Accept": "application/json, text/event-stream",
    }
    if api_key:
        headers["X-API-Key"] = api_key
    req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            remaining = resp.headers.get("X-Trial-Remaining")
    except urllib.error.HTTPError as e:
        if e.code == 402:
            print("HTTP 402 — payment required.", file=sys.stderr)
            if e.headers.get("X-Trial-Exhausted"):
                print("Trial key exhausted.", file=sys.stderr)
            print("Pay via x402 or pass a trial key (--key / CZID_API_KEY).", file=sys.stderr)
            sys.exit(402)
        raise
    # Server replies as SSE: one `data: {json}` line.
    for line in raw.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:]), remaining
    return json.loads(raw), remaining  # plain-JSON fallback


def parse_args(pairs):
    args = {}
    for p in pairs:
        k, _, v = p.partition("=")
        if "," in v:
            args[k] = v.split(",")
        elif v.isdigit():
            args[k] = v
        else:
            args[k] = v
    return args


def main():
    argv = sys.argv[1:]
    api_key = os.environ.get("CZID_API_KEY")
    if "--key" in argv:
        i = argv.index("--key")
        api_key = argv[i + 1]
        del argv[i : i + 2]
    if not argv:
        print(__doc__)
        sys.exit(1)
    tool, targs = argv[0], parse_args(argv[1:])

    _ = rpc("initialize", {"protocolVersion": "2025-11-25", "clientInfo": {"name": "python-client", "version": "0"}, "capabilities": {}}, api_key)
    result, remaining = rpc("tools/call", {"name": tool, "arguments": targs}, api_key, req_id=2)
    if remaining is not None:
        print(f"[X-Trial-Remaining: {remaining}]", file=sys.stderr)
    if "error" in result:
        print(json.dumps(result["error"], indent=2))
        sys.exit(1)
    for block in result["result"].get("content", []):
        if block.get("type") == "text":
            try:
                print(json.dumps(json.loads(block["text"]), indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(block["text"])


if __name__ == "__main__":
    main()
