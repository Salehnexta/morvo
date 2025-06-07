"""Unified Morvo Companion WebSocket Handler

This module implements WebSocket support for the unified مورفو companion,
enabling real-time chat functionality with the Gulf-friendly marketing assistant.
"""

import json
import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel, Field

from agents import UnifiedMorvoCompanion
from auth.jwt_bearer import get_current_user_ws
from config import get_settings
from protocols.manager import EnhancedProtocolManager

logger = logging.getLogger(__name__)
settings = get_settings()

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_conversation_map: Dict[str, str] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"WebSocket connection established for user {user_id}")
        
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_conversation_map:
            del self.user_conversation_map[user_id]
        logger.info(f"WebSocket connection removed for user {user_id}")
    
    async def send_message(self, user_id: str, message: Dict[str, Any]):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)
            
    def set_conversation(self, user_id: str, conversation_id: str):
        self.user_conversation_map[user_id] = conversation_id
        
    def get_conversation(self, user_id: str) -> Optional[str]:
        return self.user_conversation_map.get(user_id)


# Singleton connection manager
manager = ConnectionManager()


class WSChatMessage(BaseModel):
    """WebSocket chat message model"""
    message: str
    conversation_id: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)


async def handle_websocket(
    websocket: WebSocket, 
    user_id: str = Depends(get_current_user_ws),
    protocol_manager: EnhancedProtocolManager = None
):
    """Handle WebSocket connections for unified مورفو companion chat"""
    await manager.connect(websocket, user_id)
    
    # Initialize the unified companion
    companion = UnifiedMorvoCompanion(
        supabase_client=protocol_manager.supabase_client if protocol_manager else None,
        load_system_prompt=True
    )
    
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_text()
            try:
                chat_request = WSChatMessage.parse_raw(data)
                
                # Get or create conversation ID
                conversation_id = chat_request.conversation_id or manager.get_conversation(user_id)
                if not conversation_id:
                    conversation_id = str(uuid.uuid4())
                    manager.set_conversation(user_id, conversation_id)
                
                # Store user message in database if Supabase is available
                if protocol_manager and protocol_manager.supabase_client:
                    await protocol_manager.supabase_client.table("messages").insert({
                        "conversation_id": conversation_id,
                        "role": "user",
                        "content": chat_request.message,
                        "created_at": datetime.utcnow().isoformat()
                    }).execute()
                
                # Acknowledge receipt
                await manager.send_message(
                    user_id, 
                    {"type": "ack", "message_id": str(uuid.uuid4())}
                )
                
                # Show typing indicator
                await manager.send_message(
                    user_id, 
                    {"type": "typing", "status": "start"}
                )
                
                # Process with the unified companion
                response = await companion.process_message(
                    user_id=user_id,
                    message=chat_request.message,
                    conversation_id=conversation_id,
                    context=chat_request.context
                )
                
                # Store assistant message in database if Supabase is available
                if protocol_manager and protocol_manager.supabase_client:
                    await protocol_manager.supabase_client.table("messages").insert({
                        "conversation_id": conversation_id,
                        "role": "assistant",
                        "content": response,
                        "created_at": datetime.utcnow().isoformat()
                    }).execute()
                    
                    # Update conversation last_message_at
                    await protocol_manager.supabase_client.table("conversations").update({
                        "last_message_at": datetime.utcnow().isoformat()
                    }).eq("id", conversation_id).execute()
                
                # Stop typing indicator
                await manager.send_message(
                    user_id, 
                    {"type": "typing", "status": "stop"}
                )
                
                # Send response
                await manager.send_message(
                    user_id,
                    {
                        "type": "message",
                        "message": response,
                        "conversation_id": conversation_id,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
                
            except json.JSONDecodeError:
                await manager.send_message(
                    user_id, 
                    {"type": "error", "message": "Invalid JSON format"}
                )
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {str(e)}")
                await manager.send_message(
                    user_id, 
                    {"type": "error", "message": f"Error processing message: {str(e)}"}
                )
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(user_id)


# Add WebSocket route to FastAPI app
def configure_websocket_route(app):
    """Configure WebSocket route for the FastAPI application"""
    @app.websocket("/ws/{user_id}")
    async def websocket_endpoint(
        websocket: WebSocket, 
        user_id: str,
        protocol_manager: EnhancedProtocolManager = Depends(lambda: app.state.protocol_manager)
    ):
        await handle_websocket(websocket, user_id, protocol_manager)