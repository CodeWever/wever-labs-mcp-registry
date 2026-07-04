# Copy Blocks for MCP Registry and Directory Forms

## Name

Wever Labs

## Short description

Free Agent Store for callable MCP rails, receipt verification, proof trails, and structured agent handoffs.

## Longer description

Wever Labs provides a free Agent Store for AI agents and builders. Agents can discover callable MCP rails, run structured workflows, verify receipts, create proof trails, inspect work-history evidence, and return trusted handoff packages. The goal is simple: agents should be able to do useful work and leave behind evidence of what happened.

## Endpoint

https://weverlabs.com/api/mcp

## Descriptor

https://weverlabs.com/.well-known/mcp.json

## Repository

https://github.com/CodeWever/wever-labs-agent-client

## Tags

agents, agent-store, mcp, workflow, receipts, proof, evidence, handoffs, automation

## Server config

```json
{
  "mcpServers": {
    "wever-labs": {
      "url": "https://weverlabs.com/api/mcp",
      "description": "Free Agent Store for AI agents with callable MCP rails, receipt verification, proof trails, and structured handoffs."
    }
  }
}
```
