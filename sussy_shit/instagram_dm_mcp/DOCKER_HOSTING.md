# How to Host Instagram DM MCP Server in Docker

This guide provides step-by-step instructions for hosting and running the Instagram DM MCP server in Docker.

## Prerequisites

- Docker installed and running
- Docker Compose (usually comes with Docker Desktop)
- Instagram credentials

## Step 1: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cd /Users/pro/Documents/instagram_dm_mcp
cat > .env << EOF
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
EOF
```

**Important**: Make sure `.env` is in `.gitignore` to avoid committing credentials!

## Step 2: Build the Docker Image

```bash
# Using docker-compose (recommended)
docker-compose build

# Or using Docker directly
docker build -t instagram-dm-mcp .
```

## Step 3: Run the Container

### Option A: Using Docker Compose (Easiest)

```bash
# Start in detached mode (runs in background)
docker compose up -d

# Or start in foreground to see logs
docker-compose up
```

### Option B: Using Docker Directly

```bash
docker run -it \
  --name instagram-dm-mcp \
  -e INSTAGRAM_USERNAME=your_username \
  -e INSTAGRAM_PASSWORD=your_password \
  -v $(pwd)/sessions:/app/sessions \
  -v $(pwd)/downloads:/app/downloads \
  instagram-dm-mcp
```

### Option C: Using Makefile (Convenient)

```bash
make build  # Build the image
make run    # Start the container
```

## Step 4: Verify It's Running

```bash
# Check if container is running
docker ps

# View logs
docker-compose logs -f
# Or
docker logs -f instagram-dm-mcp

# Check container status
docker-compose ps
```

## Step 5: Connect MCP Clients

Since MCP uses **stdio** (standard input/output) for communication, connecting from MCP clients requires special configuration.

### For Cursor IDE

Update your `~/.cursor/mcp.json` to connect to the Docker container:

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

**Important Notes:**
- The container must be running before Cursor tries to connect
- Use `docker exec -i` (interactive stdin) to allow stdio communication
- The container name must match: `instagram-dm-mcp`

### For Claude Desktop

Update `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### Alternative: Wrapper Script Approach

If `docker exec` doesn't work well, create a wrapper script:

**Create `docker-mcp-wrapper.sh`:**

```bash
#!/bin/bash
docker exec -i instagram-dm-mcp python src/mcp_server.py
```

Make it executable:
```bash
chmod +x docker-mcp-wrapper.sh
```

Then use it in your MCP config:

```json
{
  "mcpServers": {
    "instagram_dms": {
      "command": "/Users/pro/Documents/instagram_dm_mcp/docker-mcp-wrapper.sh"
    }
  }
}
```

## Step 6: Restart Your MCP Client

After updating the configuration:

- **Cursor**: Restart Cursor completely
- **Claude Desktop**: Restart Claude Desktop

## Managing the Container

### View Logs
```bash
docker-compose logs -f
# Or
docker logs -f instagram-dm-mcp
```

### Stop the Container
```bash
docker-compose down
# Or
docker stop instagram-dm-mcp
```

### Start a Stopped Container
```bash
docker-compose up -d
# Or
docker start instagram-dm-mcp
```

### Restart the Container
```bash
docker-compose restart
# Or
docker restart instagram-dm-mcp
```

### Remove the Container
```bash
docker-compose down
# Or
docker rm instagram-dm-mcp
```

### Access Container Shell
```bash
docker exec -it instagram-dm-mcp /bin/bash
```

## Troubleshooting

### Container Won't Start

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Check logs for errors:**
   ```bash
   docker-compose logs
   ```

3. **Verify environment variables:**
   ```bash
   docker exec instagram-dm-mcp env | grep INSTAGRAM
   ```

### MCP Client Can't Connect

1. **Ensure container is running:**
   ```bash
   docker ps | grep instagram-dm-mcp
   ```

2. **Test the connection manually:**
   ```bash
   docker exec -i instagram-dm-mcp python src/mcp_server.py
   ```
   (This should start the MCP server - press Ctrl+C to exit)

3. **Check container name matches:**
   - Container name in `docker ps` should match the name in your MCP config
   - Default name is `instagram-dm-mcp`

4. **Verify permissions:**
   ```bash
   docker exec instagram-dm-mcp ls -la /app/sessions
   ```

### Session Files Not Persisting

1. **Check volume mounts:**
   ```bash
   docker inspect instagram-dm-mcp | grep -A 10 Mounts
   ```

2. **Verify directories exist:**
   ```bash
   ls -la sessions/
   ls -la downloads/
   ```

3. **Check permissions:**
   ```bash
   chmod 755 sessions downloads
   ```

### Authentication Issues

1. **Delete old session and restart:**
   ```bash
   rm sessions/*_session.json
   docker-compose restart
   ```

2. **Check credentials in .env:**
   ```bash
   cat .env
   ```

## Production Deployment

For production use, consider:

1. **Use Docker secrets or environment variable injection** instead of `.env` files
2. **Set resource limits** in `docker-compose.yml`:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 512M
   ```
3. **Set up health checks**
4. **Use a process manager** like systemd or supervisor
5. **Set up log rotation**

## Quick Reference

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

