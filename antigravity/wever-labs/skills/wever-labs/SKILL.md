---
name: wever-labs
description: >-
  Use Wever Labs MCP tools when an agent needs to move or hold money in USDC on
  Base (payments, escrow, refunds, disputes, payouts, invoices, work orders, and
  hiring another agent), find an MCP server or agent tool in the free Wever
  agent directory, run a diligence check on a JSON data sample, an evidence
  list or a set of MCP tool declarations, or plan a trip around a sporting
  event. Covers which Wever Labs tool fits each task, how calls are priced, and
  how humans approve spending.
---

# Wever Labs

Wever Labs is hosted MCP infrastructure for agents that work with money and
with other agents. Money moves as native USDC on Base mainnet (`eip155:8453`).
Every money step returns a signed receipt or record that the agent keeps.

This plugin connects two Wever Labs servers:

| Server | Endpoint | What it holds |
| --- | --- | --- |
| `wever-labs_mcp` | https://weverlabs.com/mcp | The main catalog: commerce rails, diligence, sports trips, Atlas asset research and more |
| `wever-labs_mcp-free` | https://weverlabs.com/mcp-free | Free, anonymous tools, including the agent directory search |

The full list of tools, with titles and prices, is in
`references/tools.md`. Read it when you need a tool that this page does not name.

## How calls are priced

- **Free tools** need no wallet or account. That covers every tool on
  `wever-labs_mcp-free`, plus free tools on the main server such as
  `edge-alert`, `fair-value`, `boutique-coupon`, `wever_boutique-list-products`
  and `wever_mandate-status`.
- **Paid tools** cost 0.10 USDC per call on Base through x402. Each wallet first
  gets 10 free calls per rolling 30 days, shared across all paid tools, and
  each of those calls carries a wallet signature. A few tools list a different
  price in their description, for example 2.00 USDC per mandate for
  `wever_mandate-issue`.
- When the free calls are used up, a paid call returns a payment-required
  response with the exact USDC terms. Show those terms to the human before
  anyone signs.
- The tool fee is separate from the money being moved. Escrow amounts, payouts
  and job fees are their own amounts with their own caps.

## Who does what

The human sets the goal and the spending limit. The human also approves and
signs every wallet request. The agent picks the tool, prepares exact inputs,
gives the human the approval or review link the tool returns, and keeps the IDs
and receipts. Use a stable `idempotency_key` wherever a tool takes one, so
retries never move money twice.

## Commerce rails on Base

Pick the rail that matches the job:

- **Hold money until work is accepted.** Use `wever_agent-escrow-lite` with
  modes `prepare_funding`, `fund_escrow`, `release_escrow`, `refund_escrow`
  and `read_escrow`. Once an unreleased escrow expires, `refund_escrow`
  returns the funds to the payer.
- **Pay a named worker for a defined task.** Work orders run in order:
  `wever_workorder-create` → `wever_workorder-fund` →
  `wever_workorder-accept` → `wever_workorder-deliver` →
  `wever_workorder-release`. Use `wever_workorder-dispute` to pause release.
  Orders go up to 25 USDC.
- **Post a fixed-fee job for another agent.** Use `wever_post-job`, then
  `wever_accept-job`, `wever_submit-work` and `wever_verify-and-release`. The
  fee is held in conditional escrow, up to 300 USDC, until the human approves
  the submitted work.
- **Refunds and disputes.** `wever_dispute-open` pauses release on a funded
  escrow or work order. Each side adds evidence with
  `wever_dispute-submit-evidence`. `wever_dispute-resolve` settles by
  releasing to the payee, refunding the payer, or splitting the locked amount.
  `wever_dispute-status` returns the full signed receipt chain. Purchases have
  their own `wever_purchase-dispute`.
- **Payouts.** Run `wever_payout-create` → `wever_payout-authorize` →
  `wever_payout-execute`, and track it with `wever_payout-status`. Execution
  returns the confirmed Base transaction hash and a signed receipt.
- **Split one payment across several recipients.** Split payments run on the
  dedicated split server at https://weverlabs.com/mcp-splits:
  `wever_split-create`, `wever_split-execute` and `wever_split-status`. A
  split pays 2 to 32 recipients, by percentages or by fixed amounts, up to
  300 USDC. Connect that server alongside this plugin when a task calls for a
  split.
- **Check a payment before and after settling.** `wever_agent-budget-guard`
  previews whether a proposed request fits the policy and budget you supply.
  `wever_x402-payment-gateway` checks a payment signature and reads the
  payer's Base USDC nonce, balance and chain time.
  `wever_payment-authority-inspector` reads a Base USDC transaction receipt
  and returns the observed payment details.
- **Invoices, purchases and balances.** `wever_agent-invoice-rail` keeps an
  issuer's invoice ledger. `wever_purchase-create-intent`,
  `wever_purchase-execute` and `wever_purchase-status` handle an approved
  purchase. `wever_treasury-balance` and `wever_treasury-flows` read a
  wallet's USDC balance and recent transfers.
- **Delegated authority.** `wever_delegated-authority` and
  `wever_mandate-issue` record exactly what a principal lets an agent do.
  `wever_mandate-halt` and `wever_mandate-revoke` are the free emergency
  controls.

## Free agent directory

Use `wever_directory-search` on `wever-labs_mcp-free` to find MCP servers,
agent tools and protocols. Pass a `query`, a `category`, or both. Each result
includes the listing's website, endpoint URL, source and verification date. The
full feed is at https://weverlabs.com/directory/index.json. Anyone can list a
server for free at https://weverlabs.com/directory/submit/, and listings that
pass the automated checks publish automatically.

To learn about a specific agent, `wever_agent-trust-check` (free) returns
source-labeled facts from Wever records: directory registration, recorded
tools, caps and delegations, and signed receipt counts.

## Diligence and data checks

Reach for these before relying on data, evidence or another server's tools:

- **JSON data sample:** `wever_data-evidence-check` returns a signed,
  field-by-field report on a sample of up to 256 KB. It checks required
  fields, empty values, types, timestamp age, source attribution and duplicate
  keys.
- **Evidence list:** `check_evidence_inventory` (free) compares the evidence
  you have with the evidence you need and lists exact matches and missing
  items. `wever_diligenceops-paid-run` is the same comparison on the main
  server.
- **MCP tool declarations:** `review_mcp_manifest` (free) or
  `wever_mcp-diligence-rail` lists missing annotations and flags actions that
  change data or spend money, before you connect a server.
- **Tokenized assets:** `wever_atlas-asset-search`,
  `wever_atlas-asset-passport`, `wever_atlas-compare` and
  `wever_atlas-rights-gap` read Atlas's sourced dataset of asset rights and
  disclosures.

Prefer the free tool when it covers the task.

## Sports trips

1. Call `wever_sports-plan-trip` with the `event`, `home_city`, `party_size`
   (1 to 8), `budget_cap_usd` and an `idempotency_key`. Add any exact provider
   quotes you already have in `quotes`. It returns an itemized itinerary
   covering flights, hotel, tickets and a dinner table, a quoted subtotal,
   budget targets and a review link for the human.
2. The human approves each exact quote at https://weverlabs.com/sports-trips/.
3. `wever_sports-book-leg` records each approved quote selection and returns a
   signed receipt. The traveler completes the reservation with the provider.
4. `wever_sports-trip-status` shows the itinerary, leg states, approvals and
   receipts. `wever_sports-cancel-leg` withdraws a selection and returns a
   signed withdrawal receipt.

For ticket prices alone, `cheapest-ticket` (free) returns the lowest listed
price for the next matching game, with its source, check time and a buy link.
`fair-value` and `edge-alert` (both free) compare prediction-market prices for
a game.

## Working pattern

1. Match the task to a section above, or search `references/tools.md`.
2. Read the tool's description. It names the contract URL with full schemas
   and limits.
3. Prepare exact inputs, including an `idempotency_key` where one is accepted.
4. Give the human any approval link, payment terms or signature request, and
   wait for their approval.
5. Keep the returned IDs, receipts and transaction hashes in your reply, so the
   human can check the work.
