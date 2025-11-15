"""
HTTP API wrapper for Instagram MCP server
This allows n8n and other HTTP clients to interact with the MCP tools via REST API
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from instagrapi import Client
from pathlib import Path
import os
import sys
import logging

# Add parent directory to path to import mcp_server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import mcp_server module - it won't execute main block when imported
import mcp_server

app = FastAPI(title="Instagram MCP HTTP API", version="1.0.0")

logger = logging.getLogger(__name__)

# Request models
class SendMessageRequest(BaseModel):
    username: str
    message: str

class SendPhotoRequest(BaseModel):
    username: str
    photo_path: str

class SendVideoRequest(BaseModel):
    username: str
    video_path: str

class ListChatsRequest(BaseModel):
    amount: int = 20
    selected_filter: str = ""
    thread_message_limit: Optional[int] = None
    full: bool = False
    fields: Optional[List[str]] = None

class ListMessagesRequest(BaseModel):
    thread_id: str
    amount: int = 20

class MarkMessageSeenRequest(BaseModel):
    thread_id: str
    message_id: str

class SearchThreadsRequest(BaseModel):
    query: str

class GetThreadByParticipantsRequest(BaseModel):
    user_ids: List[int]

class GetThreadDetailsRequest(BaseModel):
    thread_id: str
    amount: int = 20

class CheckOnlineStatusRequest(BaseModel):
    usernames: List[str]

class SearchUsersRequest(BaseModel):
    query: str

class GetUserStoriesRequest(BaseModel):
    username: str

class LikeMediaRequest(BaseModel):
    media_url: str
    like: bool = True

class GetUserFollowersRequest(BaseModel):
    username: str
    count: int = 20

class GetUserFollowingRequest(BaseModel):
    username: str
    count: int = 20

class GetUserPostsRequest(BaseModel):
    username: str
    count: int = 12

class ListMediaMessagesRequest(BaseModel):
    thread_id: str
    limit: int = 100

class DownloadMediaRequest(BaseModel):
    message_id: str
    thread_id: str
    download_path: str = "/app/downloads"

class DownloadSharedPostRequest(BaseModel):
    message_id: str
    thread_id: str
    download_path: str = "/app/downloads"

class DeleteMessageRequest(BaseModel):
    thread_id: str
    message_id: str

class MuteConversationRequest(BaseModel):
    thread_id: str
    mute: bool = True

@app.get("/")
async def root():
    return {
        "service": "Instagram MCP HTTP API",
        "version": "1.0.0",
        "endpoints": [
            "/send-message",
            "/send-photo",
            "/send-video",
            "/list-chats",
            "/list-messages",
            "/mark-seen",
            "/pending-chats",
            "/search-threads",
            "/thread-by-participants",
            "/thread-details",
            "/user-id",
            "/username",
            "/user-info",
            "/online-status",
            "/search-users",
            "/user-stories",
            "/like-media",
            "/user-followers",
            "/user-following",
            "/user-posts",
            "/list-media-messages",
            "/download-media",
            "/download-shared-post",
            "/delete-message",
            "/mute-conversation",
        ]
    }

@app.post("/send-message")
async def api_send_message(request: SendMessageRequest):
    """Send an Instagram direct message"""
    result = mcp_server.send_message(request.username, request.message)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/send-photo")
async def api_send_photo(request: SendPhotoRequest):
    """Send a photo via Instagram DM"""
    result = mcp_server.send_photo_message(request.username, request.photo_path)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/send-video")
async def api_send_video(request: SendVideoRequest):
    """Send a video via Instagram DM"""
    result = mcp_server.send_video_message(request.username, request.video_path)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/list-chats")
async def api_list_chats(request: ListChatsRequest):
    """List Instagram DM chats"""
    result = mcp_server.list_chats(
        request.amount,
        request.selected_filter,
        request.thread_message_limit,
        request.full,
        request.fields
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/list-messages")
async def api_list_messages(request: ListMessagesRequest):
    """List messages from a thread"""
    result = mcp_server.list_messages(request.thread_id, request.amount)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/mark-seen")
async def api_mark_seen(request: MarkMessageSeenRequest):
    """Mark a message as seen"""
    result = mcp_server.mark_message_seen(request.thread_id, request.message_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/pending-chats")
async def api_pending_chats(amount: int = 20):
    """List pending chats"""
    result = mcp_server.list_pending_chats(amount)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/search-threads")
async def api_search_threads(request: SearchThreadsRequest):
    """Search for threads"""
    result = mcp_server.search_threads(request.query)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/thread-by-participants")
async def api_thread_by_participants(request: GetThreadByParticipantsRequest):
    """Get thread by participant IDs"""
    result = mcp_server.get_thread_by_participants(request.user_ids)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/thread-details")
async def api_thread_details(request: GetThreadDetailsRequest):
    """Get thread details"""
    result = mcp_server.get_thread_details(request.thread_id, request.amount)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/user-id/{username}")
async def api_user_id(username: str):
    """Get user ID from username"""
    result = mcp_server.get_user_id_from_username(username)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/username/{user_id}")
async def api_username(user_id: str):
    """Get username from user ID"""
    result = mcp_server.get_username_from_user_id(user_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/user-info/{username}")
async def api_user_info(username: str):
    """Get user information"""
    result = mcp_server.get_user_info(username)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/online-status")
async def api_online_status(request: CheckOnlineStatusRequest):
    """Check user online status"""
    result = mcp_server.check_user_online_status(request.usernames)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/search-users")
async def api_search_users(request: SearchUsersRequest):
    """Search for users"""
    result = mcp_server.search_users(request.query)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/user-stories")
async def api_user_stories(request: GetUserStoriesRequest):
    """Get user stories"""
    result = mcp_server.get_user_stories(request.username)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/like-media")
async def api_like_media(request: LikeMediaRequest):
    """Like or unlike media"""
    result = mcp_server.like_media(request.media_url, request.like)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/user-followers")
async def api_user_followers(request: GetUserFollowersRequest):
    """Get user followers"""
    result = mcp_server.get_user_followers(request.username, request.count)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/user-following")
async def api_user_following(request: GetUserFollowingRequest):
    """Get users that a user is following"""
    result = mcp_server.get_user_following(request.username, request.count)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/user-posts")
async def api_user_posts(request: GetUserPostsRequest):
    """Get user posts"""
    result = mcp_server.get_user_posts(request.username, request.count)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/list-media-messages")
async def api_list_media_messages(request: ListMediaMessagesRequest):
    """List media messages in a thread"""
    result = mcp_server.list_media_messages(request.thread_id, request.limit)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/download-media")
async def api_download_media(request: DownloadMediaRequest):
    """Download media from a message"""
    result = mcp_server.download_media_from_message(
        request.message_id,
        request.thread_id,
        request.download_path
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/download-shared-post")
async def api_download_shared_post(request: DownloadSharedPostRequest):
    """Download shared post from a message"""
    result = mcp_server.download_shared_post_from_message(
        request.message_id,
        request.thread_id,
        request.download_path
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/delete-message")
async def api_delete_message(request: DeleteMessageRequest):
    """Delete a message"""
    result = mcp_server.delete_message(request.thread_id, request.message_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/mute-conversation")
async def api_mute_conversation(request: MuteConversationRequest):
    """Mute or unmute a conversation"""
    result = mcp_server.mute_conversation(request.thread_id, request.mute)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize Instagram client (shared with mcp_server)
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    
    if not username or not password:
        logger.error("INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD must be set")
        sys.exit(1)
    
    try:
        logger.info("Attempting to login to Instagram...")
        SESSIONS_DIR = Path("/app/sessions") if Path("/app/sessions").exists() else Path(".")
        SESSION_FILE = SESSIONS_DIR / f"{username}_session.json"
        if SESSION_FILE.exists():
            logger.info(f"Loading existing session from {SESSION_FILE}")
            mcp_server.client.load_settings(SESSION_FILE)
        
        mcp_server.client.login(username, password)
        mcp_server.client.dump_settings(SESSION_FILE)
        logger.info("Successfully logged in to Instagram")
        logger.info("Starting HTTP API server on 0.0.0.0:5000...")
    except Exception as e:
        logger.error(f"Failed to login to Instagram: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    
    # Run the HTTP server
    try:
        uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
    except Exception as e:
        logger.error(f"Failed to start HTTP server: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

