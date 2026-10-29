[![AllMCPs Verified](https://allmcps.com/api/badge/wever-labs-agent-products)](https://allmcps.com/mcp/wever-labs-agent-products?verify=2ebca967-c3ef-4ce8-b448-3fe60a87d96f)

# Wever Labs Agent Products

Public publication metadata for the hosted Wever Labs MCP server.

Wever Labs exposes **77 production tools** at **https://weverlabs.com/mcp** using Streamable HTTP. Tools cover bounded agent work, delegated authority, commerce, receipts and verification, handoffs, and operations. Atlas tools include `wever_atlas-asset-passport`, `wever_atlas-asset-search`, `wever_atlas-compare` and `wever_atlas-rights-gap`. Documentation: **https://weverlabs.com**.

Standard paid calls cost **0.10 USDC per call on Base mainnet via x402**. The wallet free allowance is **10 free calls per wallet per rolling 30 days**, shared across paid endpoints, not a separate allowance for each tool. Check the [live product catalog](https://weverlabs.com/api/agent-operating-products) and each tool's contract for operation-specific prices and payment requirements. Tool access does not grant payment authority or credentials; preparation and read-only operations retain their stated bounds.

The free `edge-alert` tool is included on the main endpoint. Call it with `{}` for current pregame sports winner prediction-market alerts at an estimated edge of 3 percentage points or more. Each call reads public Polymarket, Kalshi and Novig data, returns market, side, market price, estimated fair price, estimated edge and timestamp, and explicitly returns `no_alerts` when no eligible market clears the threshold. Every price names its source and uses a common $1 payout basis. Each response names checked sports, leagues, sources and coverage limits. It requires no wallet, account or x402 payment. Human page: **https://weverlabs.com/edge-alerts/**.

The free `fair-value` tool on **https://weverlabs.com/mcp** takes one prediction-market name, Kalshi or Polymarket ticker, or URL. Game names support team aliases and reversed order. It returns `needs_match` with dated outcome choices when selection is needed, or `no_match` when no open full-game winner market is returned for the teams. An exact selection returns the existing thesis model's estimated YES fair price, its original comparison and timestamps. Matched Kalshi, Polymarket and Novig quotes appear separately when available, labelled by source and observation time. Access is anonymous, with no wallet or payment. Human lookup: [weverlabs.com/fair-value/](https://weverlabs.com/fair-value/).

The separate free tier at **https://weverlabs.com/mcp-free** exposes **10 tools with no authentication, wallet, or payment required**.

The free `boutique-coupon` tool on **https://weverlabs.com/mcp** returns one shareable code for **10 percent off** at Stripe checkout across all five Rebecca Belle Boutique stores. Agents may share it freely with any human. Calling the tool needs no wallet or payment. Get the current code and redemption steps at [weverlabs.com/coupon/](https://weverlabs.com/coupon/).

`cheapest-ticket` reads public Gametime prices and compares exact NFL and NBA games with TickPick. It returns the event, lowest listed price among the working sources, check time and buy link. SeatGeek needs a server Client ID for its API; Ticketmaster Discovery needs a Consumer Key for event matches and buy links. Humans complete purchases through the returned link.

| Publication field | Value |
| --- | --- |
| Registry name | `io.github.CodeWever/wever-labs-products` |
| Title | Wever Labs Agent Products |
| Registry metadata version | `0.8.2-registry.1` |
| Hosted server version | `0.8.0` |
| Transport | Streamable HTTP |
| Remote endpoint | https://weverlabs.com/mcp |
| Production tools | 77 |
| Free endpoint | https://weverlabs.com/mcp-free (10 tools, no auth) |
| Documentation | https://weverlabs.com |
| Repository | https://github.com/CodeWever/wever-labs-mcp-registry |

The hosted server's MCP `initialize` and `tools/list` responses supply its runtime version and tool catalog. Registry metadata version `0.8.2-registry.1` refreshes discovery while the hosted server remains `0.8.0`. The descriptors record that runtime version in publisher metadata. Run `bash validation-curl.sh` before publication to verify the advertised metadata.

## Atlas rights research

Use `wever_atlas-compare` with two asset ids or tickers to compare tokenization stage, issuer involvement, custody and backing, distributions, voting, legal status and redemption. Each side retains the exact value, explanation and source references.

Use `wever_atlas-rights-gap` to list rights marked `not disclosed`, with the sources checked for each field. Filter by asset or field and page through results. Both tools read the current [Atlas asset dataset](https://atlas.weverlabs.com/api/assets) at request time and return its version, source timestamp and content digest, so updated issuer disclosures appear on the next fresh call.

## Cursor Marketplace plugin

This repository includes the `wever-labs` Cursor plugin. Its manifest is [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json), and [`mcp.json`](mcp.json) connects Cursor to the hosted Wever Labs server at `https://weverlabs.com/mcp`.

After installation, enable the Wever Labs MCP server and ask Cursor to show its available tools. The plugin uses a remote Streamable HTTP connection configured by URL. Hosted tools follow their documented input and payment contracts.

See [CURSOR_MARKETPLACE.md](CURSOR_MARKETPLACE.md) for David's submission steps and a pre-submission Cursor connection check. Plugin version `1.0.0` identifies the Cursor package independently of the hosted server version.

## Second dates

The three second-date tools open a market after a completed staked first date, accept YES or NO predictions, and resolve the outcome. Both daters approve the exact market terms through the human page before it opens. Stakes use nonredeemable play credits with no cash value, capped at 5 credits per bet and 25 credits per market. Both daters report the result. Matching reports settle the market; differing reports go to signed operator review. Winning bettors share the pool pro-rata with signed receipts. Each call costs 0.10 USDC under the existing shared free allowance, separately from play stakes.

Tools: `wever_second-date-market-open`, `wever_second-date-bet`, `wever_second-date-resolve`. Human page: [Second dates](https://weverlabs.com/second-dates/). Agent contract: [Second-date contract](https://weverlabs.com/api/second-dates-contract). This is a game between consenting adults.

## Date Safe

`wever_datesafe-scan` on **https://weverlabs.com/mcp-free** checks supplied photos and/or conversation text. It is free and anonymous, with no wallet or x402 charge. Findings are evidence-based indicators, never verdicts about a person. Reports include reviewed image-reuse matches, five conversation patterns, detectable image metadata, check limits and human next steps. Photo matches establish neither identity nor intent. See [Date Safe](https://weverlabs.com/date-safe/) for inputs and [the documented seed and review gate](https://github.com/CodeWever/wever-commerce-proof-build-week-2026/blob/main/docs/date-safe-registry.md).

## Verified single

`wever_single-credential-issue` at **https://weverlabs.com/mcp** issues a signed credential after the human signs in with Wever email sign-in, submits a current photo, and writes their single-status attestation in their own words. The agent submits the human’s short-lived issuance authorization. Issuance costs **0.10 USDC**, under the existing shared wallet free allowance. The credential includes its ID, issuance time, 12-month expiry, opaque verified sign-in identity, photo perceptual hash and verbatim attestation.

What this proves: identity was verified via Wever sign-in on the issuance date. Single status is self-attested, not independently investigated by Wever. The photo fingerprint binds the photo submitted by the holder.

`wever_single-credential-check` at **https://weverlabs.com/mcp-free** takes `credential_id` and returns `valid`, `revoked` or `expired` with the scope summary. Unknown IDs return `not_found`. Anyone can check anonymously, with no wallet or charge. Holders can revoke their credential, and a report flow records evidence for Wever operator revocation. See [Verified single](https://weverlabs.com/verified-single/), [Matchmaking](https://weverlabs.com/matchmaking/) and [Date Safe](https://weverlabs.com/date-safe/).

## Agent trust check

`wever_agent-trust-check` on **https://weverlabs.com/mcp-free** accepts an `agent_identifier`: a Wever agent ID, mailbox or registered name. Its plain-language report covers directory registration, recorded authority, signed receipts and the listed operator using Wever's own records. Every fact names its source, and missing facts say "not on file." Reports contain facts with sources, without scores or verdicts. The tool is free and anonymous, with no wallet or x402 charge. See [Agent trust check](https://weverlabs.com/trust-check/) to run a lookup or read the MCP example.


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

To use the ten anonymous free tools, use `https://weverlabs.com/mcp-free` as the URL. Run `bash validation-curl.sh` for read-only MCP discovery checks.

## Legacy endpoint

`https://weverlabs.com/api/mcp` is the legacy Labs API endpoint. It serves the four free Labs computations plus a service-catalog discovery tool. Use the production endpoint above for the current 77-tool server.

## Registry metadata

The official 2025-12-11 schema limits `description` to 100 characters. `server.json` therefore uses a short summary; the longer public description is retained above.

This server is remote-only. `server.json` has no `packages` array. `package.json` is minimal fallback metadata, not an installed MCP server or a published npm artifact. No package publication is needed for the current remote descriptor.

David performs Official MCP Registry login and publication using [PUBLISHING_RUNBOOK.md](PUBLISHING_RUNBOOK.md). After publication, follow [VERIFY_CHECKLIST.md](VERIFY_CHECKLIST.md). A GitHub push updates this repository's public metadata for downstream scanners; it does not publish an Official MCP Registry listing or confirm a directory refresh.

No secrets, keys, credentials or private implementation code belong in this repository.
