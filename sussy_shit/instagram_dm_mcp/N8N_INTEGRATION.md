# Using Instagram MCP with n8n

This guide explains how to use the Instagram MCP server with n8n workflows.

## Overview

The Instagram MCP server can run in two modes:
1. **MCP stdio mode** - For AI assistants like Claude Desktop or Cursor
2. **HTTP API mode** - For n8n and other HTTP-based automation tools

## Setup

### 1. Start the HTTP API Server

Update your `docker-compose.yml` to run the HTTP API instead of the MCP server:

```yaml
instagram_mcp:
  build: ./instagram_dm_mcp
  container_name: instagram_mcp
  restart: unless-stopped
  environment:
    - INSTAGRAM_USERNAME=your_instagram_username
    - INSTAGRAM_PASSWORD=your_instagram_password
    - MODE=http  # Set to 'http' for HTTP API mode
  volumes:
    - ./mcp_data:/app/data
    - ./mcp_data/sessions:/app/sessions
    - ./mcp_data/downloads:/app/downloads
  networks:
    - mcp-network
  ports:
    - "5001:5000"  # HTTP API will be available on port 5001
```

Or modify the entrypoint to use HTTP mode by default, or set the `MODE` environment variable.

### 2. Access the API

Once running, the HTTP API will be available at:
- **Local**: `http://localhost:5001`
- **From n8n container**: `http://instagram_mcp:5000` (using Docker network)

### 3. API Documentation

Visit `http://localhost:5001/docs` for interactive API documentation (Swagger UI).

## Using in n8n

### Method 1: HTTP Request Node

1. **Add an HTTP Request node** to your n8n workflow
2. **Configure the node**:
   - **Method**: `POST` (or `GET` for some endpoints)
   - **URL**: `http://instagram_mcp:5000/<endpoint>`
   - **Authentication**: None (internal Docker network)
   - **Body**: JSON with the required parameters

### Example: Send a Message

**HTTP Request Node Configuration:**
- **Method**: `POST`
- **URL**: `http://instagram_mcp:5000/send-message`
- **Body** (JSON):
```json
{
  "username": "target_username",
  "message": "Hello from n8n!"
}
```

### Example: List Chats

**HTTP Request Node Configuration:**
- **Method**: `POST`
- **URL**: `http://instagram_mcp:5000/list-chats`
- **Body** (JSON):
```json
{
  "amount": 20,
  "selected_filter": "",
  "full": false
}
```

### Example: Get User Info

**HTTP Request Node Configuration:**
- **Method**: `GET`
- **URL**: `http://instagram_mcp:5000/user-info/{username}`
- Replace `{username}` with the actual username

## Available Endpoints

### Messaging
- `POST /send-message` - Send a text message
- `POST /send-photo` - Send a photo
- `POST /send-video` - Send a video
- `POST /list-messages` - List messages in a thread
- `POST /mark-seen` - Mark message as seen
- `POST /delete-message` - Delete a message

### Chats/Threads
- `POST /list-chats` - List all chats
- `POST /pending-chats` - List pending chats
- `POST /search-threads` - Search for threads
- `POST /thread-details` - Get thread details
- `POST /thread-by-participants` - Get thread by user IDs
- `POST /mute-conversation` - Mute/unmute conversation

### Users
- `GET /user-info/{username}` - Get user information
- `GET /user-id/{username}` - Get user ID from username
- `GET /username/{user_id}` - Get username from user ID
- `POST /search-users` - Search for users
- `POST /online-status` - Check user online status
- `POST /user-followers` - Get user followers
- `POST /user-following` - Get users being followed
- `POST /user-posts` - Get user posts
- `POST /user-stories` - Get user stories

### Media
- `POST /like-media` - Like or unlike a post
- `POST /list-media-messages` - List media messages in thread
- `POST /download-media` - Download media from message
- `POST /download-shared-post` - Download shared post/reel

## n8n Workflow Examples

### Example 1: Auto-respond to New Messages

1. **Webhook node** (or Schedule trigger) - Trigger workflow
2. **HTTP Request node** - `POST /list-chats` with `{"selected_filter": "unread"}`
3. **Code node** - Process unread chats
4. **HTTP Request node** - `POST /list-messages` for each thread
5. **HTTP Request node** - `POST /send-message` to respond

### Example 2: Monitor User Activity

1. **Schedule trigger** - Run every hour
2. **HTTP Request node** - `POST /online-status` with list of usernames
3. **IF node** - Check if users are online
4. **HTTP Request node** - `POST /send-message` to notify

### Example 3: Download Media from Messages

1. **Schedule trigger** - Run daily
2. **HTTP Request node** - `POST /list-chats`
3. **HTTP Request node** - `POST /list-media-messages` for each thread
4. **HTTP Request node** - `POST /download-media` for each media message
5. **Save file node** - Save downloaded media

## Error Handling

All endpoints return JSON with a `success` field:
- `{"success": true, ...}` - Operation succeeded
- `{"success": false, "message": "error message"}` - Operation failed

In n8n, use an **IF node** to check the `success` field and handle errors accordingly.

## Tips

1. **Use Docker network names**: When calling from n8n container, use `http://instagram_mcp:5000` instead of `localhost`
2. **Session persistence**: The server saves Instagram sessions to `/app/sessions` - make sure this is mounted as a volume
3. **Rate limiting**: Be mindful of Instagram's rate limits when creating workflows
4. **Error handling**: Always check the `success` field in responses
5. **API docs**: Use `http://localhost:5001/docs` to explore all available endpoints interactively

## Troubleshooting

### Connection refused
- Ensure the container is running: `docker compose ps`
- Check if port 5001 is accessible
- Verify Docker network connectivity

### Authentication errors
- Check that `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD` are set correctly
- Check container logs: `docker compose logs instagram_mcp`

### Function not found errors
- Ensure you're using the correct endpoint path
- Check the API docs at `/docs` for the correct request format

