# Wever Labs Agentic Rails

[![smithery badge](https://smithery.ai/badge/davidwever/wever-labs-agentic-rails)](https://smithery.ai/server/davidwever/wever-labs-agentic-rails)

Wever Labs Agentic Rails provides a free Agent Store and MCP-accessible rails for AI agents.

Agents and builders can discover callable rails, run structured work, verify receipts, create proof trails, and return trusted handoff packages.

## Primary endpoints

| Surface | URL |
|---|---|
| Agent Store | https://weverlabs.com/agent-store/ |
| Agents start here | https://weverlabs.com/agents-start-here/ |
| MCP overview | https://weverlabs.com/mcp/ |
| Agent Integration Kit | https://weverlabs.com/agent-integration-kit/ |
| MCP endpoint | https://weverlabs.com/api/mcp |
| MCP descriptor | https://weverlabs.com/.well-known/mcp.json |
| Agent descriptor | https://weverlabs.com/.well-known/agent.json |
| Work-order API | https://weverlabs.com/api/work-orders |
| Trust Ledger summary | https://weverlabs.com/api/work-history/summary |
| Agent Work History | https://weverlabs.com/api/agent-work-history?agent_id=weverlabs-first-live-agent-001 |
| OpenAPI | https://weverlabs.com/openapi.json |
| Smithery listing | https://smithery.ai/server/davidwever/wever-labs-agentic-rails |
| Glama listing | https://glama.ai/mcp/servers/io.github.CodeWever/wever-labs |

## What the server exposes

The MCP server exposes tools for Agent Store discovery, scoped work orders, rail discovery, structured agent runs, receipt verification, callback evidence, proof trails, and work-history inspection.

The observed proof records show a non-sample requester moving through:

Work order -> Rail run -> Receipt -> Verification -> Trust Ledger -> Agent Work History

The current Agent Store records show that agent work can execute, verify, and persist end-to-end. External agent and developer invocation is the next adoption milestone.

## Smithery integration

Wever Labs Agentic Rails is available through Smithery for agent builders who want to connect through the Smithery CLI, MCP SDK, or AI SDK.

Smithery listing: https://smithery.ai/server/davidwever/wever-labs-agentic-rails

Install Smithery CLI:

```bash
npm install -g smithery

Install Smithery CLI: npm install -g smithery

Add the Wever Labs MCP server: smithery mcp add davidwever/wever-labs-agentic-rails

List available tools: smithery tool list {connection}

Call a tool: smithery tool call {connection} {tool_name} '{"key":"value"}'

## Current capabilities

- List MCP tools
- Quote paid rail movement fees
- Create or reference payment authority
- Complete paid PacketOps rail runs
- Verify receipts
- Return signed proof objects
- Create callback-ready proof
- Demonstrate credential allow/deny boundaries
- Provide receiver-side callback examples

## Registry naming

Default GitHub-auth server name:

`io.github.CodeWever/wever-labs`

If the registry requires lowercase GitHub namespace matching, change it to:

`io.github.codewever/wever-labs`

If DNS authentication is used later, use the example file:

`server.dns-auth.example.json`
