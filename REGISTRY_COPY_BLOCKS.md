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
