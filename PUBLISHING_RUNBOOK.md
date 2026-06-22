# Official MCP Registry Publishing Runbook

## What this is

This runbook prepares Wever Labs for the Official MCP Registry. PulseMCP ingests from that registry, so this is the upstream path for PulseMCP visibility.

## Before terminal work

Confirm these resolve in a browser:

- https://weverlabs.com/api/mcp
- https://weverlabs.com/.well-known/mcp.json
- https://weverlabs.com/agent-self-serve/
- https://weverlabs.com/provider-callback-receiver-examples/

Confirm directory state:

- AI Agents Directory: approved
- MCP.directory: submitted or ready from GitHub repo form
- MCP.so: submitted or in progress
- PulseMCP: waits on Official MCP Registry ingestion

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

From the local folder that contains `server.json`:

```bash
mcp-publisher login github
mcp-publisher publish
```

The login command should give you a GitHub device code. Complete that authorization in the browser, then return to terminal.

## Verification

After publish:

```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.CodeWever/wever-labs" | python3 -m json.tool
```

If the search returns no result, try lowercase namespace:

```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.codewever/wever-labs" | python3 -m json.tool
```

## If publish fails

Common errors:

- Permission error: GitHub auth namespace may need lowercase or must match the GitHub owner exactly.
- Validation error: run `mcp-publisher init` in a clean folder, compare its generated schema to `server.json`, then copy the Wever Labs values into the generated file.
- Package verification error: use `package.json` and publish a small public npm metadata package, then try again.

## Safe boundary

Do not publish secrets. Do not include Stripe keys, Supabase service-role keys, raw agent credentials, webhook secrets, or private environment variables.
