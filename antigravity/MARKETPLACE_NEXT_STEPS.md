# Antigravity Marketplace: what remains David's

The bundle at [`antigravity/wever-labs/`](wever-labs/) is complete, including its logo, and passes every offline check in strict mode ([VALIDATION.md](VALIDATION.md)). Two steps remain, in this order.

## 1. Run Google's strict validator locally

Install the Antigravity CLI ([download page](https://antigravity.google/download)):

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

From the repository root:

```bash
agy plugin validate --strict ./antigravity/wever-labs
```

The target is 0 errors and 0 warnings. Paste the full output into [VALIDATION.md](VALIDATION.md). Then do a local smoke test:

```bash
agy plugin install ./antigravity/wever-labs
```

```bash
agy plugin list --json
```

Expect skill `wever-labs` and two MCP servers. In Antigravity, check that the Wever Labs logo shows on the plugin card under **Customizations > Installed**. Run `/wever-labs`, then click the first starter prompt, which uses the free directory search.

Worth checking during the smoke test: paid tools on `/mcp` take payment and free-allowance proofs from per-request `X-Wever-Wallet-Proof` and `Payment-Signature` headers (see `/.well-known/wever-labs-mcp.json`). Antigravity's `mcp_config.json` only sets static headers. Confirm how a paid call behaves from Antigravity before describing paid flows in the submission.

## 2. Submit through the partner intake form

Submit with the [Antigravity Marketplace partner intake form](https://forms.gle/2EX5RFYPoJe1UgxR9), linked from [Build plugins → Publish](https://antigravity.google/docs/build-plugins#publish-to-the-antigravity-marketplace) and [Marketplace → Next steps](https://antigravity.google/docs/marketplace#next-steps). The form was not opened during this build, so its fields are unknown. Have these ready:

| Item | Value |
| --- | --- |
| Plugin name / display name | `wever-labs` / Wever Labs |
| Version | 1.0.0 |
| Description | Agent commerce rails on Base: USDC payments, escrow, refunds and payouts, plus a free agent directory, data diligence checks and sports-trip planning. |
| Source | https://github.com/CodeWever/wever-labs-mcp-registry, folder `antigravity/wever-labs` |
| Logo | `antigravity/wever-labs/assets/logo.svg` (same file as https://weverlabs.com/favicon.svg) |
| Homepage / author | https://weverlabs.com / Wever Labs |
| MCP endpoints | https://weverlabs.com/mcp and https://weverlabs.com/mcp-free (Streamable HTTP, no auth) |

## Optional decisions

- **Logo padding.** The mark's rounded tile is inset about 7% per side. Google recommends about 10% transparent padding. It passes every check and renders cleanly on light and dark backgrounds. If a reviewer asks for more padding, change the SVG's `viewBox` from `0 0 64 64` to `-2 -2 68 68`, which adds padding without touching the artwork.
- **One-command GitHub install.** `agy plugin install https://github.com/<owner>/<repo>` expects the plugin at the repository root. To offer it, publish this folder as its own repository. Moving the plugin to this repository's root is the other option, but it would add a root `skills/` folder that the Cursor plugin under review would also pick up.
- **Split payments.** The skill points to the dedicated server at `https://weverlabs.com/mcp-splits`. It can be wired as a third server in `mcp_config.json` if you want splits available without extra setup.
- **Stale registry counts (not changed here).** `README.md`, `DIRECTORY_STATUS.md`, `REGISTRY_COPY_BLOCKS.md`, `server.json` and `validation-curl.sh` still say 83 and 16 tools. `validation-curl.sh` now fails against the live 84.
