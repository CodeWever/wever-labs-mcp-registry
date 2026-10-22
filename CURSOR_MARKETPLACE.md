# Wever Labs for Cursor

Wever Labs connects Cursor agents to hosted tools for delegated work, commerce, receipts, verification, and handoffs.

## Plugin files

The existing public repository is the plugin root:

```text
wever-labs-mcp-registry/
  .cursor-plugin/
    plugin.json
  mcp.json
  README.md
  LICENSE
  CURSOR_MARKETPLACE.md
```

- `.cursor-plugin/plugin.json` declares the `wever-labs` Cursor plugin and points to `mcp.json`.
- `mcp.json` connects the `wever-labs` server to `https://weverlabs.com/mcp` using remote Streamable HTTP.
- Plugin version `1.0.0` identifies this distribution package. The hosted server reports its own version through MCP discovery.

The configuration consists of the remote URL. It contains no local command, arguments, environment variables, headers, credentials, or secret placeholders. Cursor infers remote transport from the URL.

Cursor's single-plugin format fits this existing repository. A dedicated repository and a multi-plugin `.cursor-plugin/marketplace.json` are not required.

## Submit to the Cursor Marketplace

David performs the Marketplace submission:

1. Sign in to the Cursor account that will own the publisher application.
2. Open [Publish a Cursor Marketplace Plugin](https://cursor.com/marketplace/publish).
3. Enter this public repository link: [CodeWever/wever-labs-mcp-registry](https://github.com/CodeWever/wever-labs-mcp-registry). Use the repository root, with the files on its default `main` branch.
4. Complete the publisher application shown after sign-in. Use the prepared metadata below wherever the application requests it, and review the detected plugin and remote MCP configuration.
5. Submit the application for Cursor's review. Cursor reviews plugins before listing them.

The public publish page currently requires sign-in and calls this a plugin publisher application. The authenticated field labels were not visible during preparation. The documented submission target is the public repository link.

| Submission metadata | Value |
| --- | --- |
| Plugin identifier | `wever-labs` |
| Product name | Wever Labs |
| Author | Wever Labs |
| Repository | https://github.com/CodeWever/wever-labs-mcp-registry |
| Homepage | https://weverlabs.com |
| Plugin version | `1.0.0` |
| License | MIT |
| Description | Connect Cursor agents to Wever Labs tools for delegated work, commerce, receipts, verification, and handoffs through the hosted MCP server. |
| MCP endpoint | https://weverlabs.com/mcp |
| Transport | Remote Streamable HTTP |

## Installation and discovery check

Once the plugin is available in Cursor, install Wever Labs from the Marketplace or Customize panel and enable its MCP server. Ask Cursor: "Show the available Wever Labs tools and summarize their descriptions." The configured server name is `wever-labs`.

For a pre-submission connection check, copy the server entry from this repository's `mcp.json` into a test workspace's `.cursor/mcp.json`, preserving other configured servers. Open that workspace in Cursor and verify that the server connects and its tools appear. This checks the endpoint connection; a plugin installation separately checks Marketplace packaging.

The hosted tools retain their operation-specific input and payment requirements. The [README](README.md) describes pricing, and the [live product catalog](https://weverlabs.com/api/agent-operating-products) provides current contracts.

## Format references

Checked on October 21, 2026 before creating the files:

- [Cursor Plugins reference](https://cursor.com/docs/reference/plugins): manifest fields, root MCP configuration, component discovery, submission checklist, and public repository submission.
- [Cursor Plugins overview](https://cursor.com/docs/plugins): installation and Marketplace review.
- [Cursor Marketplace publish page](https://cursor.com/marketplace/publish): publisher sign-in and submission entry point.

Status: plugin files prepared for David's submission. Marketplace submission, approval, and an installed Cursor plugin test remain separate steps.
