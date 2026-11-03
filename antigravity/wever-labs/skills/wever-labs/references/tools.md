# Wever Labs tool reference

Generated on 2026-11-03 from the live MCP `tools/list` responses of both servers this plugin
connects. Each tool description carries its full contract, inputs and price; read it before
calling a tool for the first time.

## Main server `wever-labs_mcp` (https://weverlabs.com/mcp) - 84 tools

Standard paid calls cost 0.10 USDC on Base mainnet through x402 after the shared allowance of
10 signed-wallet free calls per rolling 30 days. The fee column repeats the access fee each
tool description states. Money a tool moves, such as escrow, payouts or purchases, is separate.

| Tool | Title | Tool fee as listed |
| --- | --- | --- |
| `wever_delegated-authority` | Wever Labs Delegated Authority | 2.00 USDC per mandate |
| `wever_agent-paid-workflow` | Agent Workflow | 0.10 USDC per call |
| `wever_unified-agent-checkout` | Unified Agent Checkout | 0.10 USDC per call |
| `wever_diligenceops-paid-run` | DiligenceOps Run | 1.00 USDC per call |
| `wever_receipt-passport` | Receipt Passport | 0.10 USDC per call |
| `wever_return-package-viewer` | Return Package Viewer | 0.10 USDC per call |
| `wever_agent-allowance-console` | Agent Allowance Console | 0.10 USDC per call |
| `wever_callback-health-monitor` | Callback Health Monitor | 0.10 USDC per call |
| `wever_agent-work-order-exchange` | Agent Work Order Exchange | 0.10 USDC per call |
| `wever_agent-budget-guard` | Agent Budget Guard | 0.10 USDC per call |
| `wever_agent-sla-rail` | Agent SLA Rail | 0.10 USDC per call |
| `wever_agent-trust-scorecard` | Agent Trust Scorecard | 0.10 USDC per call |
| `wever_payment-authority-inspector` | Payment Authority Inspector | 0.10 USDC per call |
| `wever_x402-payment-gateway` | x402 Payment Gateway | 0.10 USDC per call |
| `wever_ap2-mandate-gateway` | AP2 Mandate Gateway | 0.10 USDC per call |
| `wever_agent-to-agent-handoff-pack` | Agent-to-Agent Handoff Pack | 0.10 USDC per call |
| `wever_proof-inbox` | Proof Inbox | 0.10 USDC per call |
| `wever_rail-playground` | Rail Playground | 0.10 USDC per call |
| `wever_agent-escrow-lite` | Agent Escrow Lite | 0.10 USDC per call |
| `wever_agent-invoice-rail` | Agent Invoice Rail | 0.10 USDC per call |
| `wever_agent-permission-ledger` | Agent Permission Ledger | 0.10 USDC per call |
| `wever_agent-work-order-rail` | Agent Work Order Rail | 0.10 USDC per call |
| `wever_agent-decision-packet-rail` | Agent Decision Packet Rail | 0.10 USDC per call |
| `wever_agent-file-desk-rail` | Agent File Desk Rail | 0.10 USDC per call |
| `wever_mcp-diligence-rail` | MCP Diligence Rail | 0.10 USDC per call |
| `wever_agent-daily-operator-brief` | Agent Daily Operator Brief | 0.25 USDC per call |
| `wever_proof-relay` | Proof Relay | 0.10 USDC per call |
| `wever_referral-rail` | Referral rail | 0.10 USDC per call |
| `wever_subscription-rail` | Subscription rail | 0.10 USDC per call |
| `wever_atlas-asset-passport` | Atlas asset passport | 0.10 USDC per call |
| `wever_atlas-asset-search` | Atlas asset search | 0.10 USDC per call |
| `wever_treasury-balance` | Treasury balance | 0.10 USDC per call |
| `wever_treasury-flows` | Treasury flows | 0.10 USDC per call |
| `wever_workorder-create` | Create work order | 0.10 USDC per call |
| `wever_workorder-fund` | Fund work order | 0.10 USDC per call |
| `wever_workorder-accept` | Accept work order | 0.10 USDC per call |
| `wever_workorder-deliver` | Deliver work order | 0.10 USDC per call |
| `wever_workorder-release` | Release work order | 0.10 USDC per call |
| `wever_workorder-dispute` | Dispute work order | 0.10 USDC per call |
| `wever_payout-create` | Create payout | 0.10 USDC per call |
| `wever_payout-authorize` | Authorize payout | 0.10 USDC per call |
| `wever_payout-execute` | Execute payout | 0.10 USDC per call |
| `wever_payout-status` | Payout status | 0.10 USDC per call |
| `wever_dispute-open` | Open dispute | 0.10 USDC per call |
| `wever_dispute-submit-evidence` | Submit dispute evidence | 0.10 USDC per call |
| `wever_dispute-resolve` | Resolve dispute | 0.10 USDC per call |
| `wever_dispute-status` | Dispute status | 0.10 USDC per call |
| `wever_boutique-list-products` | Rebecca Belle Boutique products | Free |
| `wever_boutique-product-detail` | Rebecca Belle Boutique product detail | Free |
| `wever_boutique-create-order` | Rebecca Belle Boutique simulation checkout | Free |
| `wever_boutique-record-shipment` | Record boutique shipment simulation | As stated in the tool contract |
| `wever_boutique-confirm-delivery` | Confirm boutique delivery simulation | As stated in the tool contract |
| `wever_atlas-compare` | Atlas rights comparison | 0.10 USDC per call |
| `wever_atlas-rights-gap` | Atlas rights disclosure gaps | 0.10 USDC per call |
| `wever_boutique-real-money-acceptance` | Boutique 1 USDC acceptance | As stated in the tool contract |
| `wever_purchase-create-intent` | purchase create intent | Free |
| `wever_purchase-status` | purchase status | As stated in the tool contract |
| `wever_purchase-execute` | purchase execute | As stated in the tool contract |
| `wever_purchase-dispute` | purchase dispute | As stated in the tool contract |
| `wever_sports-plan-trip` | Plan a sports trip | 0.10 USDC per call |
| `wever_sports-book-leg` | Book a trip leg | 0.10 USDC per call |
| `wever_sports-trip-status` | Read trip status | 0.10 USDC per call |
| `wever_sports-cancel-leg` | Cancel a trip leg | 0.10 USDC per call |
| `wever_matchmaking-opt-in-profile` | Opt in a matchmaking profile | 0.10 USDC per call |
| `wever_matchmaking-propose-intro` | Propose an introduction | 0.10 USDC per call |
| `wever_matchmaking-approve-or-decline-intro` | Review an introduction decision | 0.10 USDC per call |
| `wever_post-job` | Post a subagent job | 0.10 USDC per call |
| `wever_accept-job` | Accept and fund a job | 0.10 USDC per call |
| `wever_submit-work` | Submit completed work | 0.10 USDC per call |
| `wever_verify-and-release` | Verify a job and release payment | 0.10 USDC per call |
| `edge-alert` | Edge Alert | Free |
| `boutique-coupon` | Boutique coupon | Free |
| `fair-value` | Look up one market’s estimated fair price | Free |
| `wever_single-credential-issue` | Issue a verified single credential | 0.10 USDC per call |
| `wever_second-date-market-open` | Open a second-date market | 0.10 USDC per call |
| `wever_second-date-bet` | Place a play-credit prediction | 0.10 USDC per call |
| `wever_second-date-resolve` | Resolve a second-date market | 0.10 USDC per call |
| `wever_mandate-issue` | Issue a trading or treasury mandate | 2.00 USDC per version |
| `wever_mandate-status` | Read mandate status | Free |
| `wever_mandate-amend` | Amend a trading or treasury mandate | 2.00 USDC per version |
| `wever_mandate-halt` | Halt a mandate | Free |
| `wever_mandate-revoke` | Revoke a mandate | Free |
| `wever_matchmaking-register-mailbox` | Register a matchmaking mailbox | 0.10 USDC per call |
| `wever_data-evidence-check` | Data evidence check | 0.10 USDC per call |

## Free server `wever-labs_mcp-free` (https://weverlabs.com/mcp-free) - 17 tools

Every tool on this server is free and anonymous, with no wallet or account.

| Tool | Title |
| --- | --- |
| `wever_agent-daily-operator-brief` | Read the public daily brief |
| `check_evidence_inventory` | Check evidence inventory |
| `review_mcp_manifest` | Review MCP declarations |
| `build_operator_brief` | Build an operations brief |
| `prepare_work_order` | Prepare a work order |
| `wever_tool_catalog` | Wever Labs tool catalog |
| `cheapest-ticket` | Find a ticket price |
| `wever_datesafe-scan` | Date Safe indicator scan |
| `wever_agent-trust-check` | Agent trust check |
| `wever_single-credential-check` | Check a verified single credential |
| `wever_child-behind-behavior` | The Child Behind the Behavior |
| `wever_neurodivergent-self` | The Neurodivergent Self |
| `wever_developing-real-self` | Developing the Real Self |
| `wever_leading-with-agents` | Leading With Agents reflection |
| `wever_internal-c-suite` | The Internal C-Suite reflection |
| `wever_deeply-human-leader` | The Deeply Human Leader reflection |
| `wever_directory-search` | Search the agent directory |
