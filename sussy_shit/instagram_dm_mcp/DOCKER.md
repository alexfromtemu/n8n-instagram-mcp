# Running Instagram DM MCP Server with Docker

This guide explains how to run the Instagram DM MCP server in a Docker container.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)
- Instagram credentials (username and password)

## Quick Start

### Using Docker Compose (Recommended)

1. **Create a `.env` file** in the project root:
   ```bash
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   ```

2. **Build and run the container**:
   ```bash
   docker-compose up -d
   ```

3. **View logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Stop the container**:
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image**:
   ```bash
   docker build -t instagram-dm-mcp .
   ```

2. **Run the container**:
   ```bash
   docker run -it \
     -e INSTAGRAM_USERNAME=your_username \
     -e INSTAGRAM_PASSWORD=your_password \
     -v $(pwd)/sessions:/app/sessions \
     -v $(pwd)/downloads:/app/downloads \
     instagram-dm-mcp
   ```

## Configuration

### Environment Variables

The container accepts the following environment variables:

- `INSTAGRAM_USERNAME`: Your Instagram username (required)
- `INSTAGRAM_PASSWORD`: Your Instagram password (required)

### Volume Mounts

The Docker setup includes two volume mounts:

1. **`./sessions:/app/sessions`**: Persists Instagram session files across container restarts
   - This prevents you from having to re-authenticate every time
   - Session files are stored as `{username}_session.json`

2. **`./downloads:/app/downloads`**: Directory for downloaded media from messages
   - Created automatically if it doesn't exist

## Connecting to MCP Clients

Since MCP uses stdio (standard input/output) for communication, the Docker container is designed to work with MCP clients that support stdio transport.

### For Cursor/Claude Desktop

You can configure the MCP client to connect to the Docker container using stdio. However, note that:

- The container must be running
- The client needs to execute `docker exec` or use a wrapper script
- Alternatively, you can run the MCP server directly (not in Docker) for local development

### Example MCP Configuration

If you want to use Docker with Cursor, you might need a wrapper script:

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

**Note**: For local development, it's often easier to run the MCP server directly without Docker. Docker is more useful for:
- Production deployments
- Consistent environments across different machines
- Isolated execution environments

## Troubleshooting

### Container won't start

- Check that environment variables are set correctly
- Verify Docker is running: `docker ps`
- Check logs: `docker-compose logs` or `docker logs instagram-dm-mcp`

### Authentication issues

- Session files are stored in `./sessions/` directory
- If you have authentication problems, try deleting the session file and restarting
- Make sure the sessions directory is writable

### Permission errors

- Ensure the `sessions` and `downloads` directories exist and are writable
- On Linux/Mac, you may need to adjust permissions:
  ```bash
  mkdir -p sessions downloads
  chmod 755 sessions downloads
  ```

## Building for Different Platforms

To build for a specific platform (e.g., ARM64 for Apple Silicon or Raspberry Pi):

```bash
docker build --platform linux/arm64 -t instagram-dm-mcp .
```

Or for AMD64:

```bash
docker build --platform linux/amd64 -t instagram-dm-mcp .
```

## Production Considerations

For production use:

1. **Use secrets management**: Don't hardcode credentials in docker-compose.yml
2. **Use Docker secrets** or environment variable injection from a secure vault
3. **Set up health checks**: Add health check endpoints if needed
4. **Monitor logs**: Set up log aggregation
5. **Resource limits**: Add memory and CPU limits in docker-compose.yml

Example with resource limits:

```yaml
services:
  instagram-dm-mcp:
    # ... other config ...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

