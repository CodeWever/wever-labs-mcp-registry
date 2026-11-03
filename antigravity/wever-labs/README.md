# Wever Labs

Wever Labs gives Antigravity agents commerce rails on Base: USDC payments,
escrow, refunds, disputes, payouts, invoices, and work orders between agents.
The same plugin adds a free agent directory, diligence checks for data and MCP
servers, and sports-trip planning.

## What's in the plugin

| Component | Path | What it does |
| --- | --- | --- |
| MCP servers | `mcp_config.json` | Connects the hosted Wever Labs servers over remote Streamable HTTP |
| Skill | `skills/wever-labs/SKILL.md` | Teaches the agent which Wever Labs tool fits each task. Run it with `/wever-labs` |
| Tool reference | `skills/wever-labs/references/tools.md` | Every tool name, title and listed fee, generated from the live servers |
| Logo | `assets/logo.svg` | The Wever Labs mark |

## The MCP servers

Wever Labs runs a hosted MCP server at **https://weverlabs.com/mcp**. It
serves commerce, diligence, sports-trip, Atlas asset-research and operations
tools to any MCP client over Streamable HTTP. A second server at
**https://weverlabs.com/mcp-free** serves free, anonymous tools, including the
agent directory search.

| Antigravity name | Endpoint | Tools when this plugin was built (2026-11-03) |
| --- | --- | --- |
| `wever-labs_mcp` | https://weverlabs.com/mcp | 84 |
| `wever-labs_mcp-free` | https://weverlabs.com/mcp-free | 17 |

Both servers connect with a URL alone. No API key, OAuth sign-in or setup
variable is needed, so the plugin is enabled as soon as it is installed. Each
server reports its current tool list through MCP `tools/list`.

## Pricing

Standard paid calls cost **0.10 USDC per call** on Base mainnet through x402,
after a shared free allowance of **10 signed-wallet calls per rolling 30
days** across all paid tools. A few tools list their own price in their
description, such as 2.00 USDC to issue a trading or treasury mandate. All
`wever-labs_mcp-free` tools are free, and so are free main-server tools such as
`edge-alert`, `fair-value` and `boutique-coupon`. Tool fees are separate from
the money a tool moves, such as escrow, payouts or purchases.

## Install

Installing from a folder or from GitHub works without Marketplace review.

**Workspace (one project).** Copy the `wever-labs` folder into the project's
`.agents/plugins/` folder, so the manifest sits at
`<workspace>/.agents/plugins/wever-labs/plugin.json`. The plugin is active only
in that workspace.

**Global (every workspace).** Copy the folder to
`~/.gemini/config/plugins/wever-labs/`.

**Antigravity CLI from GitHub.** Clone the repository, then install the plugin
folder:

```bash
git clone https://github.com/CodeWever/wever-labs-mcp-registry.git
```

```bash
agy plugin install ./wever-labs-mcp-registry/antigravity/wever-labs
```

Check that it loaded:

```bash
agy plugin list
```

The list should show `wever-labs` with 1 skill and 2 MCP servers. In
Antigravity, open **Customizations > Installed > Wever Labs** to see its MCP
servers and skill.

## Try it

- "Search the Wever Labs agent directory for MCP servers that handle invoicing"
- "Set up a Wever Labs work order that pays a worker 20 USDC on Base after I approve delivery"
- "Plan a Wever Labs sports trip for two from Chicago to the next Packers home game under $1,500"

Antigravity asks before it runs an MCP tool unless your
[permission policy](https://antigravity.google/docs/permissions) allows that
tool or server.

## Learn more

- Wever Labs: https://weverlabs.com
- Agent-readable overview: https://weverlabs.com/llms.txt
- Product catalog and contracts: https://weverlabs.com/api/agent-operating-products
- Agent directory: https://weverlabs.com/directory/
- Source: https://github.com/CodeWever/wever-labs-mcp-registry

Licensed under MIT.
