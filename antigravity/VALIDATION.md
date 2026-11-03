# Antigravity plugin validation: `wever-labs` 1.0.0

Checked on November 3, 2026. Plugin root: [`antigravity/wever-labs/`](wever-labs/).

## Result

| Check | Result |
| --- | --- |
| `agy plugin validate --strict` | **Not run here.** `agy` is not installed in the build environment, and the environment's policy blocked downloading and running Google's CLI binary. **The strict CLI validation still needs to run on David's machine before submission.** |
| `plugin.json` against the hosted JSON schema (`https://antigravity.google/schemas/v1/plugin.json`, Draft 2020-12, fetched November 3) | Valid |
| Offline checks of every requirement in the docs (`python3 scripts/check_antigravity_plugin.py --strict --live`) | 71 checks, all pass: 0 errors, 0 warnings |
| Logo | `assets/logo.svg`: the Wever Labs mark, copied unchanged from `https://weverlabs.com/favicon.svg` |
| Unit tests (`python3 -B -m unittest discover -s tests -p 'test_*.py'`) | 56 tests pass (38 existing, 18 new) |

## Checks against Google's docs, page by page

### [Build plugins: directory structure](https://antigravity.google/docs/build-plugins#directory-structure)

| Requirement | Result |
| --- | --- |
| `plugin.json` at `<plugin-root>/plugin.json` | Pass |
| `README.md` at the plugin root for the Marketplace detail view | Pass |
| MCP servers in `<plugin-root>/mcp_config.json` | Pass |
| Skills at `skills/<skill-name>/SKILL.md`, with references in `references/` | Pass: `skills/wever-labs/SKILL.md`, `skills/wever-labs/references/tools.md` |
| Visual assets under `assets/` | Pass: `assets/logo.svg` |
| `scripts/`, `agents/`, `rules/`, `hooks.json` | Not used, so not applicable |

### [Build plugins: manifest field reference](https://antigravity.google/docs/build-plugins#field-reference) and the hosted schema

| Field | Requirement | Value | Result |
| --- | --- | --- | --- |
| keys | Only schema keys (`additionalProperties: false`) | 12 schema keys | Pass |
| `$schema` | Official schema URL | `https://antigravity.google/schemas/v1/plugin.json` | Pass |
| `name` | Lowercase kebab-case `^[a-z0-9]+(-[a-z0-9]+)*$` (doc page) and `^[a-zA-Z0-9_-]+$` (schema) | `wever-labs` | Pass, both patterns |
| `displayName` | Required for the Marketplace. No "Plugin"/"MCP" suffix, and no leading Antigravity/Gemini/Claude/Cursor | `Wever Labs` | Pass |
| `description` | Required for the Marketplace. 1 to 2 sentences, 120 to 160 characters recommended | 150 characters | Pass |
| `version` | Required for the Marketplace. Semantic versioning recommended | `1.0.0` | Pass |
| `logo` | Required for the Marketplace. Bundled relative path, `.svg/.png/.jpg/.jpeg/.webp`, 1:1, at least 128×128, about 10% transparent padding, legible in light and dark themes | `assets/logo.svg` | Pass. The SVG is square (64×64 `viewBox`) and scales to any size. It is transparent outside a rounded tile inset about 7% per side, slightly under the recommended ~10%. Rendered at 128 px, it reads clearly on white, dark gray and black backgrounds |
| `suggestedPrompts` | Recommended. At most 3 non-blank strings | 3 prompts | Pass |
| `author` | Required for the Marketplace. String or `{name, email, url}`, and `url` must be https | `{"name": "Wever Labs", "url": "https://weverlabs.com"}` | Pass |
| `homepage` | Recommended. Public https URL | `https://weverlabs.com` | Pass |
| `repository` | Public https URL | `https://github.com/CodeWever/wever-labs-mcp-registry` | Pass |
| `license` | Recommended. SPDX identifier | `MIT` | Pass |
| `keywords` | Recommended. Lowercase strings | 10 keywords | Pass |
| `skills` | Omit when using the default `skills/` folder | Omitted | Pass |

### [Build plugins: agent skills](https://antigravity.google/docs/build-plugins#agent-skills)

| Requirement | Result |
| --- | --- |
| Frontmatter `name` is kebab-case, 1 to 64 characters, and matches the folder | Pass: `wever-labs` in `skills/wever-labs/` |
| Frontmatter `description` says what the skill does and when to use it, in 1 to 1,024 characters | Pass: 484 characters |
| Optional `disable-model-invocation` | Not set (defaults to `false`), so the skill loads automatically on matching tasks |

### [Build plugins: MCP servers](https://antigravity.google/docs/build-plugins#mcp-servers) and [MCP configuration properties](https://antigravity.google/docs/mcp#mcp-configuration-properties)

| Requirement | Result |
| --- | --- |
| Root object holds only `mcpServers` | Pass |
| Each server has exactly one transport: `serverUrl` (or `url`) for remote, `command` for stdio | Pass: `serverUrl` on both servers |
| Remote servers use Streamable HTTP. Legacy HTTP+SSE and `httpUrl` are not supported | Pass: both endpoints are Streamable HTTP over https |
| Only documented properties | Pass: `serverUrl` only |
| `variables`, if used, sits inside `mcpServers.<server>`, never at the root | Not used. The server needs no credentials |
| `PLUGIN_ROOT`/`PLUGIN_DATA` are not duplicated in `env` | Not used |
| Namespacing as `<plugin-name>_<server-key>` | `wever-labs_mcp` and `wever-labs_mcp-free` |
| No OAuth configuration | Pass. The server publishes no OAuth discovery document (`/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server` return 404), so Antigravity has no sign-in to start |

### [Build plugins: pre-publish checklist](https://antigravity.google/docs/build-plugins#pre-publish-checklist-and-common-pitfalls)

| Checklist item | Result |
| --- | --- |
| Strict CLI validation exits with 0 errors and 0 warnings | **Still to run on David's machine.** The offline equivalent passes with 0 errors and 0 warnings |
| Plugin naming and branding | Pass |
| Skill folder names match frontmatter | Pass |
| Rule `globs` format | Not applicable (no rules) |
| MCP `variables` scope | Not applicable (no variables) |
| Hooks structure and paths | Not applicable (no hooks) |
| Bundled local logo and executables | Pass: `logo` points to the bundled square `assets/logo.svg`. No executables are bundled |

### [Build plugins: publish to the Antigravity Marketplace](https://antigravity.google/docs/build-plugins#publish-to-the-antigravity-marketplace)

| Requirement | Result |
| --- | --- |
| Passes `agy plugin validate --strict` | Still to run |
| `plugin.json` has `name`, `displayName`, `description`, `version`, `logo`, `suggestedPrompts` and `author` | All present |
| `README.md` | Present |
| Bundled logo asset | Present: `assets/logo.svg` |

### [Plugins: install surfaces](https://antigravity.google/docs/plugins#managing-plugins-by-surface)

The README's install notes use only documented paths: workspace `.agents/plugins/`, global `~/.gemini/config/plugins/`, and `agy plugin install <local-path>` after a `git clone`. None of these needs Marketplace review. The plugin declares no `variables`, so it installs enabled ([Build plugins: MCP servers note](https://antigravity.google/docs/build-plugins#mcp-servers)).

### Live tool discovery

`tools/list` was read from the live servers at build time. The tool reference is generated from those responses.

| Endpoint | Server info | Live tools | In `references/tools.md` |
| --- | --- | --- | --- |
| https://weverlabs.com/mcp | `io.github.CodeWever/wever-labs-products` 0.8.0 | 84 | 84, names match |
| https://weverlabs.com/mcp-free | `io.github.CodeWever/wever-labs-free` 1.0.0 | 17 | 17, names match |
| https://weverlabs.com/mcp-splits (named in the skill, not wired) | — | 3 | `wever_split-create`, `wever_split-execute` and `wever_split-status` are all live |

The live counts match the brief (84 and 17). No tool was called, and nothing was paid.

## Differences from the job brief

1. **The MCP component goes in `mcp_config.json`, not `plugin.json`.** The manifest schema has no MCP field and rejects unknown keys. Source: [build-plugins#mcp-servers](https://antigravity.google/docs/build-plugins#mcp-servers) and [schemas/v1/plugin.json](https://antigravity.google/schemas/v1/plugin.json).
2. **Two servers are wired.** `wever_directory-search`, which the skill must teach, exists only on `/mcp-free`. The docs support several servers in one `mcp_config.json`, each with its own namespace. Their own example bundles three.
3. **Not every one of the 84 main tools is a 0.10 USDC paid tool.** Live `llms.txt` splits the 84 into 68 x402-priced tools and 16 others: 2 free boutique catalog reads, the free coupon, Edge Alert and fair-value tools, 3 free mandate controls, 4 boutique simulation and acceptance tools, and 4 agent purchase tools. Of the 68 priced tools, 63 list 0.10 USDC. `wever_delegated-authority` costs 2.00 per mandate, `wever_mandate-issue`/`-amend` cost 2.00 per version with no free allowance, `wever_diligenceops-paid-run` costs 1.00, and `wever_agent-daily-operator-brief` costs 0.25. The README states 0.10 USDC as the standard price and points to the listed per-tool fees.
4. **The doc page and the hosted schema use different `name` patterns.** The doc says lowercase kebab-case, and the schema also accepts uppercase and underscores. `wever-labs` passes both.
5. **A remote logo URL is not an option for Wever Labs.** The hosted schema accepts https logo URLs only on `google.com`, `gstatic.com` or `googleusercontent.com`, so the logo is bundled as a file rather than linked.
6. **One-command GitHub install takes a repository URL** (`agy plugin install https://github.com/<owner>/<repo>`). The docs show no subfolder form, so this repo's plugin installs from GitHub by clone plus local path. See [MARKETPLACE_NEXT_STEPS.md](MARKETPLACE_NEXT_STEPS.md) for the one-command option.

Everything else in the brief matches Google's current docs: the component types, remote Streamable HTTP or stdio servers, OAuth and user variables, and GitHub or workspace distribution without review.

## Reproduce

```bash
python3 scripts/check_antigravity_plugin.py --live
```

```bash
python3 scripts/check_antigravity_plugin.py --write-reference --live
```

The second command regenerates `references/tools.md` from the live servers. Re-run it whenever the catalog changes.
