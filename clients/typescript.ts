// Minimal czid-mcp client — TypeScript, no dependencies (fetch + SSE parse).
// Run: npx tsx clients/typescript.ts company_lookup '{"id":"27082440"}'
// Env: CZID_URL (default https://czid.casuyi.com/mcp), CZID_API_KEY (trial key)

const URL = process.env.CZID_URL ?? "https://czid.casuyi.com/mcp";

type Rpc = { jsonrpc: "2.0"; id: number; method: string; params?: unknown };
type RpcResult = {
  result?: { content?: { type: string; text?: string }[] };
  error?: { code: number; message: string };
};

async function rpc(
  method: string,
  params?: unknown,
  id = 1,
  apiKey?: string,
): Promise<{ data: RpcResult; trialRemaining: string | null }> {
  const res = await fetch(URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
      ...(apiKey ? { "X-API-Key": apiKey } : {}),
    },
    body: JSON.stringify({ jsonrpc: "2.0", id, method, params } satisfies Rpc),
  });

  if (res.status === 402) {
    const challenge = await res.text();
    throw new PaymentRequiredError(challenge, res.headers.get("x-trial-exhausted") === "true");
  }
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);

  // Reply is one SSE `data: {...}` line (server is stateless, single event).
  const raw = await res.text();
  const line = raw.split("\n").find((l) => l.startsWith("data: "));
  const data = JSON.parse((line ?? raw).slice(line ? 6 : 0)) as RpcResult;
  return { data, trialRemaining: res.headers.get("x-trial-remaining") };
}

export class PaymentRequiredError extends Error {
  constructor(public challenge: string, public trialExhausted = false) {
    super(trialExhausted ? "Trial exhausted — pay via x402" : "Payment required (x402)");
    this.name = "PaymentRequiredError";
  }
}

export async function callTool(
  name: string,
  args: Record<string, unknown>,
  apiKey = process.env.CZID_API_KEY,
) {
  await rpc(
    "initialize",
    {
      protocolVersion: "2025-11-25",
      clientInfo: { name: "ts-client", version: "0" },
      capabilities: {},
    },
    0,
    apiKey,
  );
  const { data, trialRemaining } = await rpc("tools/call", { name, arguments: args }, 2, apiKey);
  if (trialRemaining) console.error(`[X-Trial-Remaining: ${trialRemaining}]`);
  if (data.error) throw new Error(`${data.error.code}: ${data.error.message}`);
  const text = data.result?.content?.find((c) => c.type === "text")?.text ?? "";
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

// CLI
if (import.meta.url === `file://${process.argv[1]}`) {
  const [tool, argsJson] = process.argv.slice(2);
  if (!tool) {
    console.error("usage: tsx typescript.ts <tool> ['{json args}']");
    process.exit(1);
  }
  const out = await callTool(tool, argsJson ? JSON.parse(argsJson) : {});
  console.log(JSON.stringify(out, null, 2));
}
