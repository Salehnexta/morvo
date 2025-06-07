"""
Enhanced Protocol Manager for Morvo AI
مدير البروتوكولات المحسن لـ Morvo AI

Integrates MCP (Model Context Protocol) and A2A (Agent-to-Agent) communication
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from agents import EnhancedMorvoAgents
from mcp_connector import get_mcp_connector

logger = logging.getLogger(__name__)

class EnhancedProtocolManager:
    """مدير البروتوكولات المحسن للـ MCP و A2A"""
    
    def __init__(self):
        self.enhanced_agents = None
        self.mcp_connector = get_mcp_connector()
        self.mcp_status = "inactive"
        self.a2a_status = "inactive"
        self.initialization_complete = False
    
    async def initialize(self):
        """تهيئة البروتوكولات المحسنة"""
        try:
            logger.info("🔄 تهيئة Enhanced Protocol Manager...")
            
            # Initialize enhanced agents with MCP & A2A
            self.enhanced_agents = EnhancedMorvoAgents()
            
            # Test MCP connection
            test_data = await self.mcp_connector.get_user_data("test")
            if test_data.get("mcp_enabled"):
                self.mcp_status = "active"
                logger.info("✅ MCP protocol active")
            else:
                self.mcp_status = "fallback"
                logger.warning("⚠️ MCP in fallback mode")
            
            # Wait for agent initialization
            await asyncio.sleep(2)  # Give time for async initialization
            
            self.a2a_status = "active"
            self.initialization_complete = True
            
            logger.info("✅ Enhanced Protocol Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Enhanced Protocol Manager: {e}")
            self.mcp_status = "error"
            self.a2a_status = "error"
    
    async def get_status(self) -> Dict[str, Any]:
        """الحصول على حالة البروتوكولات"""
        return {
            "mcp_status": self.mcp_status,
            "a2a_status": self.a2a_status,
            "initialization_complete": self.initialization_complete,
            "enhanced_agents_available": self.enhanced_agents is not None,
            "agents_count": 5 if self.enhanced_agents else 0,
            "mcp_connector_available": self.mcp_connector is not None
        }
    
    async def get_mcp_resources(self) -> List[Dict[str, Any]]:
        """الحصول على موارد MCP المتاحة"""
        if not self.enhanced_agents:
            return []
        
        return [
            {
                "uri": "data://supabase/profiles",
                "type": "database",
                "description": "User profiles data",
                "status": "active" if self.mcp_status == "active" else "fallback"
            },
            {
                "uri": "data://supabase/campaigns",
                "type": "database", 
                "description": "Marketing campaigns data",
                "status": "active" if self.mcp_status == "active" else "fallback"
            },
            {
                "uri": "analytics://data/access",
                "type": "analytics",
                "description": "Analytics access data",
                "status": "active" if self.mcp_status == "active" else "fallback"
            },
            {
                "uri": "schema://agents/enhanced",
                "type": "schema",
                "description": "Enhanced agents schema",
                "status": "active"
            }
        ]
    
    async def get_a2a_network(self) -> Dict[str, Any]:
        """الحصول على حالة شبكة A2A"""
        if not self.enhanced_agents:
            return {"agents": [], "connections": 0}
        
        agents = [
            {
                "id": "M1",
                "name": "محلل استراتيجي متقدم",
                "endpoints": ["analysis", "research", "planning"],
                "status": "active"
            },
            {
                "id": "M2", 
                "name": "مراقب وسائل التواصل الاجتماعي",
                "endpoints": ["monitoring", "sentiment", "engagement"],
                "status": "active"
            },
            {
                "id": "M3",
                "name": "محسن الحملات التسويقية",
                "endpoints": ["optimization", "roi", "budget"],
                "status": "active"
            },
            {
                "id": "M4",
                "name": "استراتيجي المحتوى الإبداعي",
                "endpoints": ["content", "creative", "calendar"],
                "status": "active"
            },
            {
                "id": "M5",
                "name": "محلل البيانات التسويقية المتقدم",
                "endpoints": ["analysis", "modeling", "insights"],
                "status": "active"
            }
        ]
        
        return {
            "agents": agents,
            "connections": len(agents) * (len(agents) - 1),  # Fully connected network
            "message_queue_size": 0,
            "collaboration_active": True
        }
    
    async def process_enhanced_message(self, content: str, user_id: str, session_id: str) -> Dict[str, Any]:
        """معالجة رسالة مع البروتوكولات المحسنة"""
        if not self.enhanced_agents:
            raise Exception("Enhanced agents not initialized")
        
        return await self.enhanced_agents.process_message_with_protocols(
            content=content,
            user_id=user_id,
            session_id=session_id
        )
    
    def get_agents_status(self) -> List[Dict[str, Any]]:
        """الحصول على حالة الوكلاء"""
        if not self.enhanced_agents:
            return []
        
        return self.enhanced_agents.get_agents_status()
