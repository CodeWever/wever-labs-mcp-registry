# Official MCP Registry verification checklist

Run the live MCP checks from the repository root before committing metadata changes. Run the Official MCP Registry checks separately after David publishes there. A Git push alone does not establish Official MCP Registry publication or downstream directory ingestion. The expected descriptor below is the current repository target, not a claim that a registry refresh has completed.

## Check the exact registry entry

```bash
curl --fail-with-body --silent --show-error --get \
  'https://registry.modelcontextprotocol.io/v0.1/servers' \
  --data-urlencode 'search=io.github.CodeWever/wever-labs-products' \
  --data-urlencode 'version=latest' \
  | python3 -m json.tool
```

Equivalent search URL:

https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.CodeWever%2Fwever-labs-products&version=latest

Search matches substrings. Inspect `servers[].server` and require an exact name match, not an older Wever entry. A correct listing contains:

```json
{
  "name": "io.github.CodeWever/wever-labs-products",
  "title": "Wever Labs Agent Products",
  "description": "29 production tools for agent work, commerce and verification; Base USDC x402 and shared free tier.",
  "version": "0.8.0",
  "websiteUrl": "https://weverlabs.com",
  "repository": {
   "url": "https://github.com/CodeWever/wever-labs-mcp-registry",
   "source": "github"
  },
  "remotes": [
   { "type": "streamable-http", "url": "https://weverlabs.com/mcp" }
  ]
}
```

- [ ] The exact server name, title, version, description, website and repository match local `server.json`.
- [ ] The remote has type `streamable-http` and URL `https://weverlabs.com/mcp`.
- [ ] There is no nonempty `packages` array. This is a remote-only server.
- [ ] The entry's `_meta["io.modelcontextprotocol.registry/official"]` reports `status: "active"` and `isLatest: true`.
- [ ] No secret or credential value appears in the listing.

For the exact version, independently query:

```bash
curl --fail-with-body --silent --show-error \
  'https://registry.modelcontextprotocol.io/v0.1/servers/io.github.CodeWever%2Fwever-labs-products/versions/0.8.0' \
  | python3 -m json.tool
```

An empty search or a 404 is not a successful publication. Check David's publisher result and the exact name/version before retrying. Do not silently change the namespace or invent a version.

## Check the advertised remote with MCP

Send a real Streamable HTTP initialize request. This checks the URL advertised by `server.json`, using the production entrance.

```bash
curl --fail-with-body --silent --show-error \
  'https://weverlabs.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"wever-registry-check","version":"1.0.0"}}}' \
  | python3 -m json.tool
```

- [ ] HTTP 200 and a JSON-RPC `result`, without `error`.
- [ ] `result.serverInfo.name` equals `io.github.CodeWever/wever-labs-products`.
- [ ] `result.serverInfo.version` equals the version in local and published `server.json` (currently `0.8.0`).
- [ ] `result.capabilities.tools` is present.

A bare GET can return 405 on this POST-based endpoint. Use successful MCP initialization as the connectivity check. The current endpoint is stateless and returns JSON; if it later negotiates sessions or SSE responses, use an MCP client that handles the advertised transport.

Optionally confirm the stateless endpoint's tool catalog:

```bash
curl --fail-with-body --silent --show-error \
  'https://weverlabs.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2025-03-26' \
  --data '{"jsonrpc":"2.0","method":"notifications/initialized"}'
curl --fail-with-body --silent --show-error \
  'https://weverlabs.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2025-03-26' \
  --data '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | python3 -m json.tool
```

- [ ] `result.tools` lists 29 production tools. Discovery verifies the advertised catalog, not successful execution of every backend.
- [ ] The separate `https://weverlabs.com/mcp-free` entrance initializes and lists 6 tools without authentication, wallet, or payment.
- [ ] Record the metadata verification date and live initialize/list results without credentials. Record Official MCP Registry publication evidence separately if publication is performed.

Run `bash validation-curl.sh` for the read-only production and free MCP checks. It verifies the production name/version against `server.json` and the 29/6 tool counts without calling tools or submitting payments.

## Publication boundaries

David runs login and publication. `package.json` is fallback metadata only; remote-only publication does not require npm publication. Third-party directory ingestion is a separate observation and is not guaranteed by these checks.

References: [Official registry quickstart](https://modelcontextprotocol.io/registry/quickstart), [remote servers](https://modelcontextprotocol.io/registry/remote-servers), [schema](https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json).
