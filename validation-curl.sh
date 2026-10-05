#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

mcp_post() {
  curl --fail-with-body --silent --show-error --connect-timeout 10 --max-time 60 \
    "$1" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -H 'MCP-Protocol-Version: 2025-03-26' \
    --data "$2"
}

for endpoint in 'https://weverlabs.com/mcp' 'https://weverlabs.com/mcp-free'; do
  echo "Checking MCP initialization: $endpoint"
  mcp_post "$endpoint" '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"wever-registry-check","version":"1.0.0"}}}' |
    python3 -c '
import json, sys
response = json.load(sys.stdin)
assert "error" not in response, response
result = response["result"]
assert "tools" in result["capabilities"], result
if sys.argv[1] == "https://weverlabs.com/mcp":
    with open("server.json") as source:
        manifest = json.load(source)
    assert result["serverInfo"]["name"] == manifest["name"], result["serverInfo"]
    assert result["serverInfo"]["version"] == manifest["version"], result["serverInfo"]
print(json.dumps(result["serverInfo"], indent=2))
' "$endpoint"

  mcp_post "$endpoint" '{"jsonrpc":"2.0","method":"notifications/initialized"}' > /dev/null
  expected_count=29
  if [[ "$endpoint" == 'https://weverlabs.com/mcp-free' ]]; then
    expected_count=6
  fi

  echo "Checking advertised tools: $endpoint"
  mcp_post "$endpoint" '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' |
    python3 -c '
import json, sys
response = json.load(sys.stdin)
assert "error" not in response, response
tools = response["result"]["tools"]
assert len(tools) == int(sys.argv[1]), f"Expected {sys.argv[1]} tools, found {len(tools)}"
print(f"Verified {len(tools)} advertised tools")
' "$expected_count"
done

echo "Read-only MCP discovery passed. No tool execution or payment was performed."
echo "Official MCP Registry publication and directory ingestion require separate verification."
