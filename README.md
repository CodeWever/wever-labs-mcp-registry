# Wever Labs MCP Registry Publishing Pack

[![smithery badge](https://smithery.ai/badge/davidwever/wever-labs-agentic-rails)](https://smithery.ai/server/davidwever/wever-labs-agentic-rails)

Wever Labs provides MCP-callable workflow rails for agents that need bounded work execution, movement-fee quotes, payment authority references, paid rail runs, structured return packages, signed receipts, callback evidence, ledger entries, and verification proof. 

## Wever Labs agent discovery links

Wever Labs exposes MCP-accessible workflow rails for proof-backed agent runs, receipts, callbacks, and handoff packages.

| Surface | URL |
|---|---|
| Website | https://weverlabs.com |
| MCP endpoint | https://weverlabs.com/api/mcp |
| MCP descriptor | https://weverlabs.com/.well-known/mcp.json |
| Free proof run | https://weverlabs.com/free-proof-run/ |
| Agent tools manifest | https://weverlabs.com/agent-tools.json |
| All agent tools | https://weverlabs.com/all-agent-tools/ |
| OpenAPI | https://weverlabs.com/openapi.json |
| LLM instructions | https://weverlabs.com/llms.txt |
| Smithery listing | https://smithery.ai/servers/davidwever/wever-labs-agentic-rails |

## Smithery integration

Wever Labs Agentic Rails is available through Smithery for agent builders who want to connect through the Smithery CLI, MCP SDK, or AI SDK.

Smithery listing: https://smithery.ai/servers/davidwever/wever-labs-agentic-rails

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
