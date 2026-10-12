# Copy Blocks for MCP Registry and Directory Forms

## Name

Wever Labs Agent Products

## Short description

29 production tools for agent work, commerce and verification; Base USDC x402 and shared free tier.

## Longer description

Wever Labs exposes 29 production MCP tools at https://weverlabs.com/mcp for agent work, delegated authority, commerce, receipts and verification, handoffs, and operations. Standard paid calls cost 0.10 USDC per call on Base mainnet via x402. A shared allowance covers 10 free calls per wallet per rolling 30 days across paid endpoints. Check each tool's contract for operation-specific prices and requirements. The separate free endpoint at https://weverlabs.com/mcp-free has 6 tools with no authentication, wallet, or payment required. Documentation is at https://weverlabs.com.

## Production server version

0.8.0

## Endpoint

https://weverlabs.com/mcp

## Free endpoint

https://weverlabs.com/mcp-free

## Documentation

https://weverlabs.com

## Repository

https://github.com/CodeWever/wever-labs-mcp-registry

## Tags

agents, mcp, commerce, x402, usdc, receipts, verification, handoffs, automation

## Server config

```json
{
  "mcpServers": {
    "wever-labs": {
      "url": "https://weverlabs.com/mcp",
      "description": "29 production tools for agent work, commerce and verification; Base USDC x402 and shared free tier."
    }
  }
}
```

---

# Prediction Market Thesis Agents

## Name

Prediction Market Thesis Agents

## Short description

Daily Kalshi and Polymarket thesis brief for agents, paid per call, with a watchlist.

## Longer description

A daily research brief on Kalshi and Polymarket markets, built for agents that act for a human. Each brief carries the Market Thesis AI engine's case for yes and for no, its bottom line, cited sources and the market price, plus updates on the caller's own watchlist, and can be emailed to the agent's human. Two tools: `thesis_latest` returns the current brief for 1.00 USDC per call through Wever Labs' x402 pay-per-call rail on Base, and `thesis_watchlist` manages watched markets at no fee. The buying agent spends within its human principal's AP2 budget; there is no subscription, and nothing is charged when no brief is available. Research, not financial advice.

## Endpoint

https://weverlabs.com/mcp-thesis

## Product contract

https://weverlabs.com/api/thesis-contract

## Tags

agents, mcp, prediction-markets, kalshi, polymarket, research, x402, usdc, pay-per-call
