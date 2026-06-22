# Copy Blocks for MCP Registry and Directory Forms

## Name

Wever Labs

## Short description

MCP-callable workflow rails for paid agent runs, receipts, callbacks, and proof.

## Longer description

Wever Labs provides MCP-callable workflow rails for agents that need movement-fee quotes, payment authority references, bounded paid rail runs, signed receipts, callback evidence, ledger entries, and verification proof. Agents can discover rails, quote a run, create or supply payment authority, execute a bounded workflow, receive a structured return package, verify the receipt, and carry proof forward through callbacks.

## Endpoint

https://weverlabs.com/api/mcp

## Descriptor

https://weverlabs.com/.well-known/mcp.json

## Repository

https://github.com/CodeWever/wever-labs-agent-client

## Tags

agents, workflow, payments, receipts, callbacks, proof, automation, mcp

## Server config

```json
{
  "mcpServers": {
    "wever-labs": {
      "url": "https://weverlabs.com/api/mcp",
      "description": "MCP-callable workflow rails for agents that need quotes, payment authority references, paid rail runs, receipts, callbacks, and proof."
    }
  }
}
```
