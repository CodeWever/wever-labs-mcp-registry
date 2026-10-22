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

For a local plugin test before submission:

1. Copy this repository's plugin files into `~/.cursor/plugins/local/wever-labs/`, preserving `.cursor-plugin/plugin.json` and root `mcp.json`.
2. Restart Cursor or run **Developer: Reload Window**.
3. Open an empty test workspace and go to **Customize**. Select **Wever Labs**, which should appear as a **Local** plugin.
4. Select **Configure wever-labs**. Confirm the source is **Plugin wever-labs**, the local environment is **Connected**, and the tool list appears.

Cursor discovers local plugins when local imports are enabled. Use a real directory for this copy; symlinks pointing outside `~/.cursor/plugins/local` are skipped. A same-name Marketplace installation takes precedence over the local copy. See [Cursor's local plugin testing instructions](https://cursor.com/docs/plugins#test-plugins-locally).

### Desktop test result

Passed on October 21, 2026 with the official Cursor desktop app 3.24.18 on macOS ARM64 and plugin version 1.0.0:

- Customize shows **Wever Labs**, **Local**, version **1.0.0**, and **57 tools enabled**.
- Server configuration shows one source, **Plugin wever-labs**, and the local environment is **Connected**.
- The plugin connects to `https://weverlabs.com/mcp` over Streamable HTTP.
- All 57 names in the desktop interface and Cursor-generated tool descriptors match the endpoint inventory. Each generated descriptor is attributed to `wever-labs`.
- The installed manifest and MCP configuration match commit `843d56010cc4502ab404047bb209f2d616befe39`. The test workspace and user profile have no direct MCP configuration supplying this server.

This verifies local plugin loading, connection, and tool discovery. No tool execution or model prompt was needed. Marketplace submission and approval remain David's next steps.

The hosted tools retain their operation-specific input and payment requirements. The [README](README.md) describes pricing, and the [live product catalog](https://weverlabs.com/api/agent-operating-products) provides current contracts.

## Format references

Checked on October 21, 2026 before creating the files:

- [Cursor Plugins reference](https://cursor.com/docs/reference/plugins): manifest fields, root MCP configuration, component discovery, submission checklist, and public repository submission.
- [Cursor Plugins overview](https://cursor.com/docs/plugins): installation and Marketplace review.
- [Cursor Marketplace publish page](https://cursor.com/marketplace/publish): publisher sign-in and submission entry point.

Status: local desktop plugin test passed. Files are ready for David's Marketplace submission and Cursor's review.
