"""
MCP Supabase Connector for Morvo AI
موصل MCP-Supabase المبسط
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

# Supabase integration
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

logger = logging.getLogger(__name__)

class SimpleMCPConnector:
    """موصل MCP مبسط لـ Supabase"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.cache: Dict[str, Any] = {}
        self._init_client()
    
    def _init_client(self):
        """تهيئة عميل Supabase"""
        if not SUPABASE_AVAILABLE:
            return
            
        try:
            url = os.getenv('SUPABASE_URL')
            key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
            
            if url and key:
                self.client = create_client(url, key)
                logger.info("✅ MCP Connector initialized")
        except Exception as e:
            logger.error(f"❌ MCP Connector error: {e}")
    
    async def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """الحصول على بيانات المستخدم"""
        if not self.client:
            return {}
        
        try:
            # Get profile
            profile_response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            
            # Get campaigns
            campaigns_response = self.client.table("marketing_campaigns").select("*").eq("user_id", user_id).limit(20).execute()
            
            # Get analytics
            analytics_response = self.client.table("analytics_data").select("*").eq("user_id", user_id).limit(50).execute()
            
            return {
                "profile": profile_response.data[0] if profile_response.data else {},
                "campaigns": campaigns_response.data or [],
                "analytics": analytics_response.data or [],
                "total_campaigns": len(campaigns_response.data) if campaigns_response.data else 0,
                "mcp_enabled": True
            }
        except Exception as e:
            logger.error(f"❌ Error getting user data: {e}")
            return {"mcp_enabled": False, "error": str(e)}
    
    async def save_conversation(self, user_id: str, content: str, response: str, context: Dict = None):
        """حفظ المحادثة مع السياق"""
        if not self.client:
            return
        
        try:
            conversation_data = {
                "user_id": user_id,
                "message": content,
                "response": response,
                "context_data": context or {},
                "created_at": datetime.now().isoformat()
            }
            
            self.client.table("morvo_conversations").insert(conversation_data).execute()
            logger.info("💾 Conversation saved to Supabase")
        except Exception as e:
            logger.error(f"❌ Error saving conversation: {e}")

# Global connector
_connector = None

def get_mcp_connector():
    global _connector
    if _connector is None:
        _connector = SimpleMCPConnector()
    return _connector
