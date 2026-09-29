# Official MCP Registry Publishing Runbook

## What this is

This runbook prepares Wever Labs for the Official MCP Registry. PulseMCP ingests from that registry, so this is the upstream path for PulseMCP visibility.

## Before terminal work

The current server is `io.github.CodeWever/wever-labs-products` at
`https://weverlabs.com/mcp`. Use the MCP POST initialize check in
[VERIFY_CHECKLIST.md](VERIFY_CHECKLIST.md) to confirm the live version matches
`server.json` and `package.json`. A bare GET is not the MCP connectivity test.

`server.json` uses the official 2025-12-11 schema and a description of at most
100 characters. The longer public description is in README.md. Validate against
that schema before committing any descriptor change.

This is a remote-only publication with no `packages` array. `package.json` is
fallback metadata only, not a requirement to publish an npm package.

## Recommended repo strategy

Preferred: create a small public repo named `wever-labs-mcp-registry` or `wever-labs-mcp` under `CodeWever`.

Include only:

- README.md
- server.json
- package.json
- PUBLISHING_RUNBOOK.md
- VERIFY_CHECKLIST.md

This avoids mixing the registry publishing surface with app code or private implementation details.

## Install publisher

On macOS, first try Homebrew:

```bash
brew install mcp-publisher
mcp-publisher --help
```

If Homebrew does not work, use the release binary:

```bash
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher
sudo mv mcp-publisher /usr/local/bin/
mcp-publisher --help
```

## Publish flow

David runs these commands himself from the local folder that contains `server.json`:

```bash
mcp-publisher login github
mcp-publisher publish
```

The login command should give you a GitHub device code. Complete that authorization in the browser, then return to terminal.

## Verification

After publication, follow [VERIFY_CHECKLIST.md](VERIFY_CHECKLIST.md). It includes
the exact registry search, the expected descriptor and a live MCP initialize
check. The required name is `io.github.CodeWever/wever-labs-products`; keep its
case and suffix intact.

## If publish fails

Common errors:

- Permission error: verify that David authenticated as the GitHub owner authorized for `io.github.CodeWever/wever-labs-products`. Do not change the namespace without reviewing the actual error.
- Validation error: run `mcp-publisher init` in a clean folder, compare its generated schema to `server.json`, then copy the Wever Labs values into the generated file.
- Package verification error: first confirm the descriptor has no `packages` array and the publisher supports remote-only servers. Only consider the fallback package metadata if a genuine package requirement is established; package publication is a separate action, not part of this preparation.

## Safe boundary

Do not publish secrets. Do not include Stripe keys, Supabase service-role keys, raw agent credentials, webhook secrets, or private environment variables.
