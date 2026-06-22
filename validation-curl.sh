#!/usr/bin/env bash
set -euo pipefail

echo "Checking Wever Labs MCP endpoint..."
curl -s "https://weverlabs.com/api/mcp" | python3 -m json.tool | head -80

echo "Checking well-known MCP descriptor..."
curl -s "https://weverlabs.com/.well-known/mcp.json" | python3 -m json.tool | head -80

echo "Checking registry search after publish..."
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.CodeWever/wever-labs" | python3 -m json.tool
