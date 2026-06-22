# Wever Labs MCP Registry Verification Checklist

## Pre-publish checks

- [ ] `server.json` has no secrets.
- [ ] `server.json` uses the intended name: `io.github.CodeWever/wever-labs`.
- [ ] `https://weverlabs.com/api/mcp` resolves.
- [ ] `https://weverlabs.com/.well-known/mcp.json` resolves.
- [ ] `https://github.com/CodeWever/wever-labs-agent-client` is public.
- [ ] The live $0.50 demo has passed recently.
- [ ] Callback receiver examples resolve.
- [ ] Credential dry run resolves.

## Post-publish checks

- [ ] Registry search returns Wever Labs.
- [ ] PulseMCP eventually ingests the registry listing.
- [ ] MCP.directory listing is checked after 24 hours.
- [ ] MCP.so listing is checked after review.
- [ ] AI Agents Directory remains approved.

## Public routing

Agents should land here:

https://weverlabs.com/agent-self-serve/

Investors should land here:

https://weverlabs.com/investor-demo/

Provider builders should land here:

https://weverlabs.com/provider-callback-receiver-examples/
