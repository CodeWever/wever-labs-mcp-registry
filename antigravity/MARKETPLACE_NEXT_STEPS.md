# Antigravity Marketplace: what remains David's

The bundle at [`antigravity/wever-labs/`](wever-labs/) is built and checked offline ([VALIDATION.md](VALIDATION.md)). Three steps remain, in this order.

## 1. Add the logo (Marketplace blocker)

The repository has no logo file, so none is bundled. Requirements from [Google's field reference](https://antigravity.google/docs/build-plugins#field-reference):

- 1:1 square, as `.svg`, `.png`, `.jpg`, `.jpeg` or `.webp`
- at least **128×128 px**, with about **10% transparent padding**
- legible on both light and dark themes
- bundled inside the plugin. Remote logo URLs are accepted only on Google domains

Existing candidates on weverlabs.com (not in this repository, and not bundled):

- `https://weverlabs.com/favicon.svg`: square SVG, transparent outside a rounded dark tile, with about 7% inset per side. This is the closest fit. Check the padding and how it reads on a dark background.
- `https://weverlabs.com/icon-512.png`: 512×512 RGBA, but opaque to every edge with no transparent padding, so it does not meet the padding rule as is.

Once approved, save the file as `antigravity/wever-labs/assets/logo.svg` (or `.png`) and add `"logo": "assets/logo.svg"` to `plugin.json`. Then confirm with:

```bash
python3 scripts/check_antigravity_plugin.py --strict --live
```

## 2. Run Google's strict validator locally

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

Expect skill `wever-labs` and two MCP servers. In Antigravity, run `/wever-labs`, then click the first starter prompt, which uses the free directory search.

Worth checking during the smoke test: paid tools on `/mcp` take payment and free-allowance proofs from per-request `X-Wever-Wallet-Proof` and `Payment-Signature` headers (see `/.well-known/wever-labs-mcp.json`). Antigravity's `mcp_config.json` only sets static headers. Confirm how a paid call behaves from Antigravity before describing paid flows in the submission.

## 3. Submit through the partner intake form

Submit with the [Antigravity Marketplace partner intake form](https://forms.gle/2EX5RFYPoJe1UgxR9), linked from [Build plugins → Publish](https://antigravity.google/docs/build-plugins#publish-to-the-antigravity-marketplace) and [Marketplace → Next steps](https://antigravity.google/docs/marketplace#next-steps). The form was not opened during this build, so its fields are unknown. Have these ready:

| Item | Value |
| --- | --- |
| Plugin name / display name | `wever-labs` / Wever Labs |
| Version | 1.0.0 |
| Description | Agent commerce rails on Base: USDC payments, escrow, refunds and payouts, plus a free agent directory, data diligence checks and sports-trip planning. |
| Source | https://github.com/CodeWever/wever-labs-mcp-registry, folder `antigravity/wever-labs` |
| Homepage / author | https://weverlabs.com / Wever Labs |
| MCP endpoints | https://weverlabs.com/mcp and https://weverlabs.com/mcp-free (Streamable HTTP, no auth) |

## Optional decisions

- **One-command GitHub install.** `agy plugin install https://github.com/<owner>/<repo>` expects the plugin at the repository root. To offer it, publish this folder as its own repository. Moving the plugin to this repository's root is the other option, but it would add a root `skills/` folder that the Cursor plugin under review would also pick up.
- **Split payments.** The skill points to the dedicated server at `https://weverlabs.com/mcp-splits`. It can be wired as a third server in `mcp_config.json` if you want splits available without extra setup.
- **Stale registry counts (not changed here).** `README.md`, `DIRECTORY_STATUS.md`, `REGISTRY_COPY_BLOCKS.md`, `server.json` and `validation-curl.sh` still say 83 and 16 tools. `validation-curl.sh` now fails against the live 84.
