# Instagram MCP Server with n8n Integration

This project provides an Instagram Direct Message MCP (Model Context Protocol) server that can be used with AI assistants (like Claude Desktop) or integrated with n8n workflows via HTTP API.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Services](#running-the-services)
- [Using with n8n](#using-with-n8n)
- [Using with AI Assistants (MCP Mode)](#using-with-ai-assistants-mcp-mode)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Docker** (version 20.10 or later)
   - Download from: https://www.docker.com/products/docker-desktop
   - Verify installation: `docker --version`

2. **Docker Compose** (version 2.0 or later)
   - Usually included with Docker Desktop
   - Verify installation: `docker compose version`

3. **Git** (optional, for cloning the repository)
   - Download from: https://git-scm.com/downloads

### System Requirements

- **macOS, Linux, or Windows** (with WSL2 for Windows)
- **At least 2GB of free disk space**
- **At least 4GB of RAM** (recommended 8GB)
- **Internet connection** for downloading Docker images and dependencies

## Installation

### Step 1: Set Up Environment Variables

**Before starting, you must configure your Instagram credentials:**

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Instagram credentials:
   ```bash
   nano .env
   # or use your preferred editor
   ```

3. Update the values in `.env`:
   ```env
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   MODE=http
   ```

**⚠️ Important:** The `.env` file contains sensitive credentials and is excluded from version control. Never commit it!

### Step 2: Clone or Download the Repository

If you have the repository:
```bash
cd /path/to/sussy_shit
```

Or if you need to set it up from scratch, ensure you have the following structure:
```
sussy_shit/
├── .env                    # Your credentials (create from .env.example)
├── .env.example            # Template file
├── docker-compose.yml
├── instagram_dm_mcp/
│   ├── Dockerfile
│   ├── docker-entrypoint.sh
│   ├── requirements.txt
│   └── src/
│       ├── mcp_server.py
│       └── http_api.py
├── mcp_data/
└── n8n_data/
```

### Step 3: Verify Docker is Running

```bash
docker ps
```

If you get an error, start Docker Desktop and wait for it to fully start.

### Step 4: Create Required Directories

The directories will be created automatically, but you can create them manually:

```bash
mkdir -p mcp_data/sessions mcp_data/downloads n8n_data
```

## Configuration

The configuration is handled via the `.env` file (set up in Installation Step 1). 

**Important Security Notes:** 
- ✅ The `.env` file is already in `.gitignore` - it won't be committed to version control
- ✅ Never commit your credentials to version control
- ✅ Keep your `.env` file secure and don't share it
- ✅ Use `.env.example` as a template for others

### Choose Your Mode

The Instagram MCP server can run in two modes:

1. **HTTP Mode** (for n8n): Set `MODE=http`
   - Exposes REST API endpoints
   - Accessible via HTTP requests
   - Best for automation workflows

2. **MCP Mode** (for AI assistants): Set `MODE=mcp` or omit the variable
   - Uses stdio transport
   - For Claude Desktop, Cursor, etc.
   - Not accessible via HTTP

For n8n integration, use `MODE=http`.

## Running the Services

### Start All Services

```bash
docker compose up -d
```

This will:
- Build the Instagram MCP server image (first time only)
- Pull the n8n image (first time only)
- Start both containers in the background

### Check Service Status

```bash
docker compose ps
```

You should see both services running:
```
NAME            STATUS
instagram_mcp   Up
n8n             Up
```

### View Logs

**View all logs:**
```bash
docker compose logs -f
```

**View Instagram MCP logs only:**
```bash
docker compose logs -f instagram_mcp
```

**View n8n logs only:**
```bash
docker compose logs -f n8n
```

### Stop Services

```bash
docker compose down
```

### Restart Services

```bash
docker compose restart
```

### Rebuild After Code Changes

If you modify the Instagram MCP code:

```bash
docker compose build instagram_mcp
docker compose up -d instagram_mcp
```

## Using with n8n

### Step 1: Access n8n

1. Open your browser and navigate to: `http://localhost:5678`
2. If this is your first time, you'll be prompted to create an account
3. Complete the setup wizard

### Step 2: Create a Workflow

1. Click **"Add workflow"** or **"New workflow"**
2. Add an **HTTP Request** node

### Step 3: Configure HTTP Request Node

**Important:** When calling from n8n (which runs in Docker), use the Docker service name, not `localhost`.

**Base URL:** `http://instagram_mcp:5000`

#### Example 1: Send a Message

1. **Method:** `POST`
2. **URL:** `http://instagram_mcp:5000/send-message`
3. **Body Content Type:** `JSON`
4. **Body:**
   ```json
   {
     "username": "target_username",
     "message": "Hello from n8n!"
   }
   ```

#### Example 2: List Chats

1. **Method:** `POST`
2. **URL:** `http://instagram_mcp:5000/list-chats`
3. **Body:**
   ```json
   {
     "amount": 20,
     "selected_filter": "unread"
   }
   ```

#### Example 3: Get User Info

1. **Method:** `GET`
2. **URL:** `http://instagram_mcp:5000/user-info/target_username`
   (Replace `target_username` with the actual username)

### Step 4: Test Your Workflow

1. Click **"Execute Workflow"** or **"Test workflow"**
2. Check the response - it should contain `"success": true` if successful

### Common n8n Workflow Patterns

#### Auto-respond to New Messages

1. **Schedule Trigger** - Run every 5 minutes
2. **HTTP Request** - `POST /list-chats` with `{"selected_filter": "unread"}`
3. **Code Node** - Process unread chats
4. **HTTP Request** - `POST /list-messages` for each thread
5. **HTTP Request** - `POST /send-message` to respond

#### Monitor User Activity

1. **Schedule Trigger** - Run every hour
2. **HTTP Request** - `POST /online-status` with usernames list
3. **IF Node** - Check if users are online
4. **HTTP Request** - `POST /send-message` to notify

## Using with AI Assistants (MCP Mode)

If you want to use this with Claude Desktop or Cursor instead of n8n:

1. Set `MODE=mcp` in `docker-compose.yml` (or remove the MODE variable)
2. Restart the container: `docker compose restart instagram_mcp`
3. Configure your MCP client to connect to the container

See `instagram_dm_mcp/DOCKER_HOSTING.md` for detailed MCP client configuration.

## API Documentation

### Interactive API Docs

Once the HTTP API is running, visit:
- **Swagger UI:** `http://localhost:5001/docs`
- **ReDoc:** `http://localhost:5001/redoc`

### Available Endpoints

#### Messaging
- `POST /send-message` - Send a text message
- `POST /send-photo` - Send a photo
- `POST /send-video` - Send a video
- `POST /list-messages` - List messages in a thread
- `POST /mark-seen` - Mark message as seen
- `POST /delete-message` - Delete a message

#### Chats/Threads
- `POST /list-chats` - List all chats
- `POST /pending-chats` - List pending chats
- `POST /search-threads` - Search for threads
- `POST /thread-details` - Get thread details
- `POST /thread-by-participants` - Get thread by user IDs
- `POST /mute-conversation` - Mute/unmute conversation

#### Users
- `GET /user-info/{username}` - Get user information
- `GET /user-id/{username}` - Get user ID from username
- `GET /username/{user_id}` - Get username from user ID
- `POST /search-users` - Search for users
- `POST /online-status` - Check user online status
- `POST /user-followers` - Get user followers
- `POST /user-following` - Get users being followed
- `POST /user-posts` - Get user posts
- `POST /user-stories` - Get user stories

#### Media
- `POST /like-media` - Like or unlike a post
- `POST /list-media-messages` - List media messages in thread
- `POST /download-media` - Download media from message
- `POST /download-shared-post` - Download shared post/reel

### Response Format

All endpoints return JSON:

**Success:**
```json
{
  "success": true,
  "message": "Operation completed",
  ...
}
```

**Error:**
```json
{
  "success": false,
  "message": "Error description"
}
```

## Troubleshooting

### Container Won't Start

**Check Docker is running:**
```bash
docker ps
```

**Check logs:**
```bash
docker compose logs instagram_mcp
```

**Common issues:**
- Port 5001 already in use: Change the port mapping in `docker-compose.yml`
- Port 5678 already in use: Change n8n port mapping
- Out of disk space: `docker system prune -a`

### Connection Errors in n8n

**"Connection cannot be established" error:**

1. **Verify the URL is correct:**
   - ✅ Use: `http://instagram_mcp:5000`
   - ❌ Don't use: `http://localhost:5001` (from n8n container)

2. **Check containers are on same network:**
   ```bash
   docker network inspect sussy_shit_mcp-network
   ```
   Both `n8n` and `instagram_mcp` should be listed.

3. **Test connectivity from n8n container:**
   ```bash
   docker compose exec n8n wget -O- http://instagram_mcp:5000/
   ```

### Instagram Login Fails

**Check credentials:**
```bash
docker compose logs instagram_mcp | grep -i "login\|error"
```

**Common issues:**
- Wrong username/password
- Instagram requires 2FA verification
- Account temporarily locked
- Rate limiting

**Solution:** Wait a few minutes and try again, or check your Instagram account status.

### API Returns Errors

**Check API is running:**
```bash
curl http://localhost:5001/
```

**Check logs:**
```bash
docker compose logs instagram_mcp --tail 50
```

**Verify MODE is set to http:**
```bash
docker compose exec instagram_mcp env | grep MODE
```

Should show: `MODE=http`

### Port Already in Use

**Change ports in docker-compose.yml:**
```yaml
ports:
  - "5002:5000"  # Change 5001 to 5002
```

Then update n8n URLs to use the new port.

### Rebuild Everything

If you're having persistent issues:

```bash
# Stop everything
docker compose down

# Remove volumes (WARNING: This deletes data)
docker compose down -v

# Rebuild
docker compose build --no-cache

# Start fresh
docker compose up -d
```

## Project Structure

```
sussy_shit/
├── README.md                    # This file
├── docker-compose.yml           # Docker Compose configuration
├── instagram_dm_mcp/            # Instagram MCP server
│   ├── Dockerfile              # Docker image definition
│   ├── docker-entrypoint.sh    # Container startup script
│   ├── requirements.txt        # Python dependencies
│   ├── src/
│   │   ├── mcp_server.py       # MCP server (stdio mode)
│   │   └── http_api.py         # HTTP API (for n8n)
│   ├── N8N_INTEGRATION.md      # Detailed n8n guide
│   └── N8N_QUICK_START.md      # Quick n8n reference
├── mcp_data/                    # Persistent data (sessions, downloads)
│   ├── sessions/               # Instagram session files
│   └── downloads/              # Downloaded media
└── n8n_data/                    # n8n data directory
```

## Additional Resources

- **n8n Documentation:** https://docs.n8n.io
- **Instagram MCP Server:** See `instagram_dm_mcp/readme.md`
- **Docker Documentation:** https://docs.docker.com

## Support

For issues specific to:
- **Instagram MCP Server:** Check `instagram_dm_mcp/` directory for documentation
- **n8n Integration:** See `instagram_dm_mcp/N8N_INTEGRATION.md`
- **Docker Issues:** Check Docker logs and documentation

## License

See individual component licenses in their respective directories.

