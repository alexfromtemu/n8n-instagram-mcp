#!/bin/bash
# Wrapper script to connect MCP clients to the Docker container
# This allows MCP clients (Cursor, Claude Desktop) to communicate with the container via stdio

# Check if container is running
if ! docker ps | grep -q instagram-dm-mcp; then
    echo "Error: Container 'instagram-dm-mcp' is not running" >&2
    echo "Start it with: docker-compose up -d" >&2
    exit 1
fi

# Execute the MCP server in the container with interactive stdin
docker exec -i instagram-dm-mcp python src/mcp_server.py

