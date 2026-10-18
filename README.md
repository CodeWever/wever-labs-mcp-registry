[![AllMCPs Verified](https://allmcps.com/api/badge/wever-labs-agent-products)](https://allmcps.com/mcp/wever-labs-agent-products?verify=2ebca967-c3ef-4ce8-b448-3fe60a87d96f)

# Wever Labs Agent Products

Public publication metadata for the hosted Wever Labs MCP server.

Wever Labs exposes **39 production tools** at **https://weverlabs.com/mcp** using Streamable HTTP. Tools cover bounded agent work, delegated authority, commerce, receipts and verification, handoffs, and operations. The production tools now include the Atlas tools `wever_atlas-asset-passport` and `wever_atlas-asset-search`. Documentation: **https://weverlabs.com**.

Standard paid calls cost **0.10 USDC per call on Base mainnet via x402**. The wallet free allowance is **10 free calls per wallet per rolling 30 days**, shared across paid endpoints, not a separate allowance for each tool. Check the [live product catalog](https://weverlabs.com/api/agent-operating-products) and each tool's contract for operation-specific prices and payment requirements. Tool access does not grant payment authority or credentials; preparation and read-only operations retain their stated bounds.

The separate free tier at **https://weverlabs.com/mcp-free** exposes **6 tools with no authentication, wallet, or payment required**.

| Publication field | Value |
| --- | --- |
| Registry name | `io.github.CodeWever/wever-labs-products` |
| Title | Wever Labs Agent Products |
| Version | `0.8.0` |
| Transport | Streamable HTTP |
| Remote endpoint | https://weverlabs.com/mcp |
| Production tools | 39 |
| Free endpoint | https://weverlabs.com/mcp-free (6 tools, no auth) |
| Documentation | https://weverlabs.com |
| Repository | https://github.com/CodeWever/wever-labs-mcp-registry |

The version and production tool count were verified against the live endpoint's MCP `initialize` and `tools/list` responses on October 6, 2026. Recheck them before a later publication.

## Connect

Use the production endpoint in a client that supports remote Streamable HTTP MCP servers:

```json
{
  "mcpServers": {
    "wever-labs": {
      "url": "https://weverlabs.com/mcp"
    }
  }
}
```

To use the six anonymous free tools, use `https://weverlabs.com/mcp-free` as the URL. Run `bash validation-curl.sh` for read-only MCP discovery checks.

## Legacy endpoint

`https://weverlabs.com/api/mcp` is the legacy Labs API endpoint. It serves the four free Labs computations plus a service-catalog discovery tool. Use the production endpoint above for the current 39-tool server.

## Registry metadata

The official 2025-12-11 schema limits `description` to 100 characters. `server.json` therefore uses a short summary; the longer public description is retained above.

This server is remote-only. `server.json` has no `packages` array. `package.json` is minimal fallback metadata, not an installed MCP server or a published npm artifact. No package publication is needed for the current remote descriptor.

David performs Official MCP Registry login and publication using [PUBLISHING_RUNBOOK.md](PUBLISHING_RUNBOOK.md). After publication, follow [VERIFY_CHECKLIST.md](VERIFY_CHECKLIST.md). A GitHub push updates this repository's public metadata for downstream scanners; it does not publish an Official MCP Registry listing or confirm a directory refresh.

No secrets, keys, credentials or private implementation code belong in this repository.

## Prediction Market Thesis Agents

A second, separate server descriptor lives in [`thesis-agents/server.json`](thesis-agents/server.json). It is not part of the 39-tool production server above.

| Publication field | Value |
| --- | --- |
| Registry name | `io.github.CodeWever/thesis-agents` |
| Title | Prediction Market Thesis Agents |
| Version | `0.1.0` |
| Transport | Streamable HTTP |
| Remote endpoint | https://weverlabs.com/mcp-thesis |
| Tools | 2: `thesis_latest` (paid per call), `thesis_watchlist` (no fee) |
| Product contract | https://weverlabs.com/api/thesis-contract |

One product: a daily research brief on Kalshi and Polymarket markets from the Market Thesis AI engine, with a per-caller watchlist, returned in the response and optionally emailed to the agent's human. `thesis_latest` costs 1.00 USDC per call by default (the live price is in the contract), paid through the existing Wever x402 pay-per-call rail on Base mainnet, the same path as `wever_diligenceops-paid-run`. The buying agent spends within its human principal's AP2 budget. No subscription, no free calls, and nothing is charged when no brief is available. Research, not financial advice.

Publish it from its own folder after the endpoint is deployed and its live `initialize` reports `io.github.CodeWever/thesis-agents` at version `0.1.0`:

```bash
cd thesis-agents
mcp-publisher login github
mcp-publisher publish
```

Live checks, read-only and without payment (`thesis_latest` without a Payment-Signature returns its 402 terms and charges nothing):

```bash
curl --fail-with-body --silent --show-error 'https://weverlabs.com/mcp-thesis' \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"wever-registry-check","version":"1.0.0"}}}' | python3 -m json.tool
curl --fail-with-body --silent --show-error 'https://weverlabs.com/mcp-thesis' \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python3 -c 'import json,sys; print([t["name"] for t in json.load(sys.stdin)["result"]["tools"]])'
curl --silent --show-error 'https://weverlabs.com/api/thesis-contract' | python3 -c 'import json,sys; print(json.load(sys.stdin)["pricing"]["price_atomic"])'
curl --silent --show-error -X POST 'https://weverlabs.com/api/thesis-agents/latest' -H 'Content-Type: application/json' --data '{}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["accepts"][0]["amount"])'
```
