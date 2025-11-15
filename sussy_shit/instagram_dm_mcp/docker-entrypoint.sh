#!/bin/bash
# Ensure credentials are set
if [ -z "$INSTAGRAM_USERNAME" ] || [ -z "$INSTAGRAM_PASSWORD" ]; then
  echo "INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD must be set!"
  exit 1
fi

# Check mode: 'http' for HTTP API, 'mcp' (or unset) for MCP stdio mode
MODE=${MODE:-mcp}

if [ "$MODE" = "http" ]; then
  # Start HTTP API server for n8n and other HTTP clients
  echo "Starting Instagram MCP HTTP API server..."
  python src/http_api.py
else
  # Start MCP server (uses stdio transport for AI assistants)
  echo "Starting Instagram MCP server (stdio mode)..."
  python src/mcp_server.py --username "$INSTAGRAM_USERNAME" --password "$INSTAGRAM_PASSWORD"
fi