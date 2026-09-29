# Wever Labs Agent Products

Public publication metadata for the hosted Wever Labs MCP server.

Agent commerce rails on weverlabs.com: 27 MCP tools, 10 production services including delegated authority with signed mandates, five planning and settlement tools, and four x402 USDC-paid endpoints on Base mainnet. Four Labs API computations free; MCP tools include 10 free calls per wallet per 30 days.

The catalog lists 10 production services and 17 explicitly disclosed unavailable historical demo backends. The five planning tools prepare or suggest results; they do not execute payments or delivery. Delegated authority creates durable work-order records under signed mandates and credential-bound grants; it does not execute the requested work or authorize payment. The four paid endpoints use x402 with USDC on Base mainnet. Their wallet free tier is shared across those four endpoints, not ten calls for every tool.

| Publication field | Value |
| --- | --- |
| Registry name | `io.github.CodeWever/wever-labs-products` |
| Title | Wever Labs Agent Products |
| Version | `0.4.0` |
| Transport | Streamable HTTP |
| Remote endpoint | https://weverlabs.com/mcp |
| Website | https://weverlabs.com |
| Repository | https://github.com/CodeWever/wever-labs-mcp-registry |

The version was read from the live endpoint's MCP `initialize` response. Recheck it before a later publication.

The official 2025-12-11 schema limits `description` to 100 characters. `server.json` therefore uses a short summary; the longer public description is retained above.

This server is remote-only. `server.json` has no `packages` array. `package.json` is minimal fallback metadata, not an installed MCP server or a published npm artifact. No package publication is needed for the current remote descriptor.

David performs publisher login and publication using [PUBLISHING_RUNBOOK.md](PUBLISHING_RUNBOOK.md). After publication, follow [VERIFY_CHECKLIST.md](VERIFY_CHECKLIST.md). Committing this repository does not publish an Official MCP Registry listing.

No secrets, keys, credentials or private implementation code belong in this repository.
