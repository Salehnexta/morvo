"""
MCP Connector for Morvo AI
موصل MCP لـ Morvo AI

Handles integration with Model Context Protocol and Supabase
"""

import os
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Optional imports with graceful handling
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.warning("⚠️ Supabase Python client not available")

class MCPConnector:
    """موصل بروتوكول سياق النماذج لمورفو"""
    
    def __init__(self):
        self.supabase_client = None
        self._initialize_connector()
    
    def _initialize_connector(self):
        """تهيئة موصل MCP"""
        try:
            if SUPABASE_AVAILABLE:
                url = os.getenv('SUPABASE_URL')
                key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
                if url and key:
                    self.supabase_client = create_client(url, key)
                    logger.info("✅ MCP Connector initialized with Supabase")
                else:
                    logger.warning("⚠️ Missing Supabase credentials for MCP Connector")
            else:
                logger.warning("⚠️ Supabase client not available for MCP Connector")
                
        except Exception as e:
            logger.error(f"❌ Error initializing MCP Connector: {e}")
    
    async def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """استرجاع بيانات المستخدم وسياق التسويق من Supabase"""
        user_data = {
            "user_id": user_id,
            "mcp_enabled": False,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            if not self.supabase_client:
                return user_data
            
            # Get user profile
            profile_response = self.supabase_client.table("profiles").select("*").eq("user_id", user_id).execute()
            if profile_response.data:
                user_data["profile"] = profile_response.data[0]
                user_data["mcp_enabled"] = True
            
            # Get campaigns
            campaigns_response = self.supabase_client.table("campaigns").select("*").eq("user_id", user_id).execute()
            if campaigns_response.data:
                user_data["campaigns"] = campaigns_response.data
            
            # Get analytics
            analytics_response = self.supabase_client.table("analytics").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(10).execute()
            if analytics_response.data:
                user_data["analytics"] = analytics_response.data
            
            # Get content performance
            content_response = self.supabase_client.table("content_performance").select("*").eq("user_id", user_id).order("engagement", desc=True).limit(5).execute()
            if content_response.data:
                user_data["content_performance"] = content_response.data
            
            # Get SEO data
            seo_response = self.supabase_client.table("seo_data").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(10).execute()
            if seo_response.data:
                user_data["seo_data"] = seo_response.data
                
            logger.info(f"✅ User data loaded via MCP for user {user_id}")
            return user_data
            
        except Exception as e:
            logger.error(f"❌ Error loading user data via MCP: {e}")
            return user_data
    
    async def save_conversation(self, user_id: str, content: str, response: str, context: Dict[str, Any] = None) -> bool:
        """حفظ المحادثة في Supabase"""
        try:
            if not self.supabase_client:
                return False
                
            conversation_data = {
                "user_id": user_id,
                "user_message": content,
                "ai_response": response,
                "companion": "مورفو",  # Unified companion name
                "created_at": datetime.now().isoformat(),
                "context_summary": str(context)[:500] if context else None  # Truncate to avoid data issues
            }
            
            # Insert conversation record
            result = self.supabase_client.table("conversations").insert(conversation_data).execute()
            
            if result.data:
                logger.info(f"✅ Conversation saved via MCP for user {user_id}")
                return True
            else:
                logger.warning(f"⚠️ Failed to save conversation for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error saving conversation via MCP: {e}")
            return False

# Singleton instance
_mcp_connector = None

def get_mcp_connector() -> MCPConnector:
    """الحصول على نسخة وحيدة من موصل MCP"""
    global _mcp_connector
    if _mcp_connector is None:
        _mcp_connector = MCPConnector()
    return _mcp_connector
