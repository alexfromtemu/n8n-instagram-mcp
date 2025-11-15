# Quick Start: Hosting in Docker

## 1. Create `.env` file

```bash
cd /Users/pro/Documents/instagram_dm_mcp
cat > .env << EOF
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
EOF
```

## 2. Build and Start

```bash
# Option A: Using Makefile (easiest)
make build
make run

# Option B: Using docker-compose
docker-compose build
docker-compose up -d

# Option C: Using Docker directly
docker build -t instagram-dm-mcp .
docker run -d --name instagram-dm-mcp \
  -e INSTAGRAM_USERNAME=your_username \
  -e INSTAGRAM_PASSWORD=your_password \
  -v $(pwd)/sessions:/app/sessions \
  -v $(pwd)/downloads:/app/downloads \
  instagram-dm-mcp
```

## 3. Verify It's Running

```bash
docker ps | grep instagram-dm-mcp
docker-compose logs -f
```

## 4. Connect MCP Client (Cursor)

Update `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "instagram_dms": {
      "command": "/Users/pro/Documents/instagram_dm_mcp/docker-mcp-wrapper.sh"
    }
  }
}
```

Or use docker exec directly:

```json
{
  "mcpServers": {
    "instagram_dms": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "instagram-dm-mcp",
        "python",
        "src/mcp_server.py"
      ]
    }
  }
}
```

## 5. Restart Cursor

Fully quit and restart Cursor for the changes to take effect.

## Common Commands

```bash
make logs      # View logs
make stop      # Stop container
make shell     # Open shell in container
make restart   # Restart container
```

## Troubleshooting

**Container not running?**
```bash
docker-compose up -d
```

**Can't connect from MCP client?**
- Make sure container is running: `docker ps`
- Check logs: `docker-compose logs`
- Verify container name matches: `instagram-dm-mcp`

**Session issues?**
```bash
rm sessions/*_session.json
docker-compose restart
```

For detailed instructions, see [DOCKER_HOSTING.md](DOCKER_HOSTING.md).

