# Quick Start: Instagram MCP with n8n

## Step 1: Update docker-compose.yml

Add the `MODE=http` environment variable to enable HTTP API mode:

```yaml
instagram_mcp:
  build: ./instagram_dm_mcp
  container_name: instagram_mcp
  restart: unless-stopped
  environment:
    - INSTAGRAM_USERNAME=your_instagram_username
    - INSTAGRAM_PASSWORD=your_instagram_password
    - MODE=http  # Enable HTTP API mode for n8n
  volumes:
    - ./mcp_data:/app/data
    - ./mcp_data/sessions:/app/sessions
    - ./mcp_data/downloads:/app/downloads
  networks:
    - mcp-network
  ports:
    - "5001:5000"  # HTTP API accessible on port 5001
```

## Step 2: Rebuild and Start

```bash
docker compose build instagram_mcp
docker compose up -d
```

## Step 3: Verify API is Running

Visit `http://localhost:5001/docs` in your browser to see the interactive API documentation.

## Step 4: Use in n8n

### Basic Example: Send a Message

1. In n8n, add an **HTTP Request** node
2. Configure:
   - **Method**: `POST`
   - **URL**: `http://instagram_mcp:5000/send-message`
   - **Body Content Type**: `JSON`
   - **Body**:
     ```json
     {
       "username": "target_username",
       "message": "Hello from n8n!"
     }
     ```

### Example: List Chats

1. Add an **HTTP Request** node
2. Configure:
   - **Method**: `POST`
   - **URL**: `http://instagram_mcp:5000/list-chats`
   - **Body**:
     ```json
     {
       "amount": 20
     }
     ```

## Available Endpoints

All endpoints return JSON with `{"success": true/false, ...}`

### Most Common:
- `POST /send-message` - Send DM
- `POST /list-chats` - List conversations
- `POST /list-messages` - Get messages from thread
- `GET /user-info/{username}` - Get user profile

See `http://localhost:5001/docs` for full API documentation.

## Tips

- Use `http://instagram_mcp:5000` (not localhost) when calling from n8n container
- Always check the `success` field in responses
- Session files are saved automatically for persistent login

