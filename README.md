[![AllMCPs Verified](https://allmcps.com/api/badge/wever-labs-agent-products)](https://allmcps.com/mcp/wever-labs-agent-products?verify=2ebca967-c3ef-4ce8-b448-3fe60a87d96f)

# Wever Labs Agent Products

Public publication metadata for the hosted Wever Labs MCP server.

Wever Labs exposes **72 production tools** at **https://weverlabs.com/mcp** using Streamable HTTP. Tools cover bounded agent work, delegated authority, commerce, receipts and verification, handoffs, and operations. Atlas tools include `wever_atlas-asset-passport`, `wever_atlas-asset-search`, `wever_atlas-compare` and `wever_atlas-rights-gap`. Documentation: **https://weverlabs.com**.

Standard paid calls cost **0.10 USDC per call on Base mainnet via x402**. The wallet free allowance is **10 free calls per wallet per rolling 30 days**, shared across paid endpoints, not a separate allowance for each tool. Check the [live product catalog](https://weverlabs.com/api/agent-operating-products) and each tool's contract for operation-specific prices and payment requirements. Tool access does not grant payment authority or credentials; preparation and read-only operations retain their stated bounds.

The free `edge-alert` tool is included on the main endpoint. Call it with `{}` for current pregame NBA full-game winner prediction-market alerts at an estimated edge of 3 percentage points or more. Each call reads public Polymarket and Kalshi data, returns market, side, market price, estimated fair price, estimated edge and timestamp, and explicitly returns `no_alerts` when no eligible market clears the threshold. It requires no wallet, account or x402 payment. Human page: **https://weverlabs.com/edge-alerts/**.

The separate free tier at **https://weverlabs.com/mcp-free** exposes **7 tools with no authentication, wallet, or payment required**.

The free `boutique-coupon` tool on **https://weverlabs.com/mcp** returns one shareable code for **10 percent off** at Stripe checkout across all five Rebecca Belle Boutique stores. Agents may share it freely with any human. Calling the tool needs no wallet or payment. Get the current code and redemption steps at [weverlabs.com/coupon/](https://weverlabs.com/coupon/).

`cheapest-ticket` reads public Gametime prices and compares exact NFL and NBA games with TickPick. It returns the event, lowest listed price among the working sources, check time and buy link. SeatGeek needs a server Client ID for its API; Ticketmaster Discovery needs a Consumer Key for event matches and buy links. Humans complete purchases through the returned link.

| Publication field | Value |
| --- | --- |
| Registry name | `io.github.CodeWever/wever-labs-products` |
| Title | Wever Labs Agent Products |
| Version | `0.8.0` |
| Transport | Streamable HTTP |
| Remote endpoint | https://weverlabs.com/mcp |
| Production tools | 72 |
| Free endpoint | https://weverlabs.com/mcp-free (7 tools, no auth) |
| Documentation | https://weverlabs.com |
| Repository | https://github.com/CodeWever/wever-labs-mcp-registry |

The hosted server's MCP `initialize` and `tools/list` responses supply the version and tool catalog. Run `bash validation-curl.sh` before publication to verify the advertised metadata.

## Atlas rights research

Use `wever_atlas-compare` with two asset ids or tickers to compare tokenization stage, issuer involvement, custody and backing, distributions, voting, legal status and redemption. Each side retains the exact value, explanation and source references.

Use `wever_atlas-rights-gap` to list rights marked `not disclosed`, with the sources checked for each field. Filter by asset or field and page through results. Both tools read the current [Atlas asset dataset](https://atlas.weverlabs.com/api/assets) at request time and return its version, source timestamp and content digest, so updated issuer disclosures appear on the next fresh call.

## Cursor Marketplace plugin

This repository includes the `wever-labs` Cursor plugin. Its manifest is [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json), and [`mcp.json`](mcp.json) connects Cursor to the hosted Wever Labs server at `https://weverlabs.com/mcp`.

After installation, enable the Wever Labs MCP server and ask Cursor to show its available tools. The plugin uses a remote Streamable HTTP connection configured by URL. Hosted tools follow their documented input and payment contracts.

See [CURSOR_MARKETPLACE.md](CURSOR_MARKETPLACE.md) for David's submission steps and a pre-submission Cursor connection check. Plugin version `1.0.0` identifies the Cursor package independently of the hosted server version.

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

To use the seven anonymous free tools, use `https://weverlabs.com/mcp-free` as the URL. Run `bash validation-curl.sh` for read-only MCP discovery checks.

## Legacy endpoint

`https://weverlabs.com/api/mcp` is the legacy Labs API endpoint. It serves the four free Labs computations plus a service-catalog discovery tool. Use the production endpoint above for the current 72-tool server.

## Registry metadata

The official 2025-12-11 schema limits `description` to 100 characters. `server.json` therefore uses a short summary; the longer public description is retained above.

This server is remote-only. `server.json` has no `packages` array. `package.json` is minimal fallback metadata, not an installed MCP server or a published npm artifact. No package publication is needed for the current remote descriptor.

David performs Official MCP Registry login and publication using [PUBLISHING_RUNBOOK.md](PUBLISHING_RUNBOOK.md). After publication, follow [VERIFY_CHECKLIST.md](VERIFY_CHECKLIST.md). A GitHub push updates this repository's public metadata for downstream scanners; it does not publish an Official MCP Registry listing or confirm a directory refresh.

No secrets, keys, credentials or private implementation code belong in this repository.
