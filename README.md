# Wever Labs Agent Products

Public publication metadata for the hosted Wever Labs MCP server.

Wever Labs exposes **29 production tools** at **https://weverlabs.com/mcp** using Streamable HTTP. Tools cover bounded agent work, delegated authority, commerce, receipts and verification, handoffs, and operations. Documentation: **https://weverlabs.com**.

Standard paid calls cost **0.10 USDC per call on Base mainnet via x402**. The wallet free allowance is **10 free calls per wallet per rolling 30 days**, shared across paid endpoints, not a separate allowance for each tool. Check the [live product catalog](https://weverlabs.com/api/agent-operating-products) and each tool's contract for operation-specific prices and payment requirements. Tool access does not grant payment authority or credentials; preparation and read-only operations retain their stated bounds.

The separate free tier at **https://weverlabs.com/mcp-free** exposes **6 tools with no authentication, wallet, or payment required**.

| Publication field | Value |
| --- | --- |
| Registry name | `io.github.CodeWever/wever-labs-products` |
| Title | Wever Labs Agent Products |
| Version | `0.8.0` |
| Transport | Streamable HTTP |
| Remote endpoint | https://weverlabs.com/mcp |
| Production tools | 29 |
| Free endpoint | https://weverlabs.com/mcp-free (6 tools, no auth) |
| Documentation | https://weverlabs.com |
| Repository | https://github.com/CodeWever/wever-labs-mcp-registry |

The version and tool counts were verified against the live endpoints' MCP `initialize` and `tools/list` responses on October 5, 2026. Recheck them before a later publication.

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

`https://weverlabs.com/api/mcp` is the legacy Labs API endpoint. It serves the four free Labs computations plus a service-catalog discovery tool. Use the production endpoint above for the current 29-tool server.

## Registry metadata

The official 2025-12-11 schema limits `description` to 100 characters. `server.json` therefore uses a short summary; the longer public description is retained above.

This server is remote-only. `server.json` has no `packages` array. `package.json` is minimal fallback metadata, not an installed MCP server or a published npm artifact. No package publication is needed for the current remote descriptor.

David performs Official MCP Registry login and publication using [PUBLISHING_RUNBOOK.md](PUBLISHING_RUNBOOK.md). After publication, follow [VERIFY_CHECKLIST.md](VERIFY_CHECKLIST.md). A GitHub push updates this repository's public metadata for downstream scanners; it does not publish an Official MCP Registry listing or confirm a directory refresh.

No secrets, keys, credentials or private implementation code belong in this repository.
