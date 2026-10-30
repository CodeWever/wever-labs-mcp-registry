# Copy Blocks for MCP Registry and Directory Forms

## Name

Wever Labs Agent Products

## Short description

83 production tools for agent work, commerce and verification; Base USDC x402 and shared free tier.

## Longer description

Wever Labs exposes 83 production MCP tools at https://weverlabs.com/mcp for agent work, delegated authority, commerce, receipts and verification, handoffs, and operations. Atlas compares two assets across tokenization stage and six rights fields, and lists disclosure gaps with the sources checked for each field. These reads follow the current Atlas dataset as coverage and issuer disclosures change. The free fair-value lookup matches one prediction-market name to dated outcome choices, then returns the existing model's estimated fair price with its original comparison and timestamps. Exact matched Kalshi, Polymarket and Novig quotes are labelled separately by source when available. Standard paid calls cost 0.10 USDC per call on Base mainnet via x402. A shared allowance covers 10 free calls per wallet per rolling 30 days across paid endpoints. Check each tool's contract for operation-specific prices and requirements. The separate free endpoint at https://weverlabs.com/mcp-free has 16 tools with no authentication, wallet, or payment required. Documentation is at https://weverlabs.com.

## Registry metadata version

0.8.2-registry.2

## Hosted server version

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
      "description": "83 production tools for agent work, commerce and verification; Base USDC x402 and shared free tier."
    }
  }
}
```
