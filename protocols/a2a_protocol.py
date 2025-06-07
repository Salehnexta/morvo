"""
Enhanced Agent-to-Agent (A2A) Protocol
بروتوكول متقدم للتواصل بين الوكلاء

Secure communication between AI agents with authentication and message tracking
"""

import logging
import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
# Make Redis import optional
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class EnhancedA2AProtocol:
    """Enhanced Agent-to-Agent Protocol Handler with Security"""
    
    def __init__(self, session: aiohttp.ClientSession, redis_client: Optional[Any] = None):
        self.session = session
        self.redis_client = redis_client if REDIS_AVAILABLE else None
        self.endpoints: Dict[str, Dict] = {}
        self.authentication_tokens: Dict[str, str] = {}
        # Additional properties expected by main_new.py
        self.agents: Dict[str, Dict] = {}  # For compatibility with main_new.py
        self.network_id: str = f"morvo_network_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.message_queue: List[Dict] = []  # Message queue for tracking
        
    async def register_agent(
        self, 
        agent_id: str, 
        endpoint: str, 
        capabilities: List[str],
        auth_token: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """تسجيل وكيل محسن مع المصادقة"""
        registration_data = {
            "endpoint": endpoint,
            "capabilities": capabilities,
            "last_seen": datetime.now().isoformat(),
            "status": "active",
            "metadata": metadata or {}
        }
        
        if auth_token:
            self.authentication_tokens[agent_id] = auth_token
            
        self.endpoints[agent_id] = registration_data
        # Also store in agents dict for main_new.py compatibility
        self.agents[agent_id] = registration_data
        
        # Cache in Redis if available
        if self.redis_client and REDIS_AVAILABLE:
            await self.redis_client.setex(
                f"agent:{agent_id}",
                3600,  # 1 hour TTL
                json.dumps(registration_data)
            )
            
        logger.info(f"Enhanced agent {agent_id} registered with endpoint {endpoint}")
        
    async def send_secure_message(
        self, 
        from_agent: str, 
        to_agent: str, 
        message: Dict[str, Any],
        require_auth: bool = True
    ) -> Dict[str, Any]:
        """إرسال رسالة آمنة بين الوكلاء"""
        try:
            if to_agent not in self.endpoints:
                raise HTTPException(status_code=404, detail=f"Agent {to_agent} not found")
                
            endpoint_data = self.endpoints[to_agent]
            endpoint = endpoint_data["endpoint"]
            
            # Prepare secure payload
            payload = {
                "from": from_agent,
                "to": to_agent,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "message_id": hashlib.sha256(
                    f"{from_agent}{to_agent}{datetime.now().isoformat()}".encode()
                ).hexdigest()[:16]
            }
            
            # Add to message queue for tracking
            self.message_queue.append({
                "id": payload["message_id"],
                "from": from_agent,
                "to": to_agent,
                "timestamp": payload["timestamp"],
                "status": "pending"
            })
            
            headers = {"Content-Type": "application/json"}
            
            # Add authentication if required
            if require_auth and to_agent in self.authentication_tokens:
                headers["Authorization"] = f"Bearer {self.authentication_tokens[to_agent]}"
                
            async with self.session.post(
                f"{endpoint}/receive", 
                json=payload,
                headers=headers,
                timeout=30
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Update message status in queue
                    for msg in self.message_queue:
                        if msg["id"] == payload["message_id"]:
                            msg["status"] = "delivered"
                            break
                    
                    # Log successful communication
                    if self.redis_client and REDIS_AVAILABLE:
                        await self.redis_client.lpush(
                            f"communication_log:{from_agent}",
                            json.dumps({
                                "to": to_agent,
                                "status": "success",
                                "timestamp": payload["timestamp"],
                                "message_id": payload["message_id"]
                            })
                        )
                        
                    return result
                else:
                    # Update message status in queue
                    for msg in self.message_queue:
                        if msg.get("id") == payload["message_id"]:
                            msg["status"] = "failed"
                            break
                            
                    raise HTTPException(
                        status_code=response.status, 
                        detail=f"Failed to send message: {response.reason}"
                    )
                    
        except Exception as e:
            logger.error(f"A2A secure message failed: {str(e)}")
            
            # Update message status in queue
            for msg in self.message_queue:
                if msg.get("id") == payload.get("message_id"):
                    msg["status"] = "error"
                    break
            
            # Log failed communication
            if self.redis_client and REDIS_AVAILABLE:
                await self.redis_client.lpush(
                    f"communication_log:{from_agent}",
                    json.dumps({
                        "to": to_agent,
                        "status": "error",
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
                )
                
            raise HTTPException(status_code=500, detail=str(e))

    def get_network_status(self) -> Dict[str, Any]:
        """الحصول على حالة الشبكة"""
        return {
            "network_id": self.network_id,
            "registered_agents": len(self.agents),
            "agents": list(self.agents.keys()),
            "message_queue_size": len(self.message_queue),
            "active_connections": len([a for a in self.agents.values() if a.get("status") == "active"]),
            "last_activity": max([a.get("last_seen", "") for a in self.agents.values()]) if self.agents else None
        }

    async def cleanup_message_queue(self, max_size: int = 1000):
        """تنظيف قائمة الرسائل للحفاظ على الأداء"""
        if len(self.message_queue) > max_size:
            # Keep only the most recent messages
            self.message_queue = self.message_queue[-max_size:]
            logger.info(f"Message queue cleaned up, kept {max_size} recent messages")

    async def broadcast_message(self, from_agent: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """بث رسالة لجميع الوكلاء المسجلين"""
        results = {}
        
        for agent_id in self.agents.keys():
            if agent_id != from_agent:  # Don't send to self
                try:
                    result = await self.send_secure_message(from_agent, agent_id, message)
                    results[agent_id] = {"status": "success", "result": result}
                except Exception as e:
                    results[agent_id] = {"status": "error", "error": str(e)}
                    
        return {
            "broadcast_id": hashlib.sha256(f"{from_agent}{datetime.now().isoformat()}".encode()).hexdigest()[:16],
            "from": from_agent,
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "total_sent": len(results),
            "successful": len([r for r in results.values() if r["status"] == "success"]),
            "failed": len([r for r in results.values() if r["status"] == "error"])
        }

    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """الحصول على حالة وكيل محدد"""
        if agent_id not in self.agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
            
        agent_data = self.agents[agent_id]
        
        # Get recent messages for this agent
        recent_messages = [
            msg for msg in self.message_queue[-100:]  # Last 100 messages
            if msg.get("from") == agent_id or msg.get("to") == agent_id
        ]
        
        return {
            "agent_id": agent_id,
            "endpoint": agent_data.get("endpoint"),
            "capabilities": agent_data.get("capabilities", []),
            "status": agent_data.get("status"),
            "last_seen": agent_data.get("last_seen"),
            "metadata": agent_data.get("metadata", {}),
            "recent_activity": {
                "messages_sent": len([m for m in recent_messages if m.get("from") == agent_id]),
                "messages_received": len([m for m in recent_messages if m.get("to") == agent_id]),
                "last_message": recent_messages[-1] if recent_messages else None
            }
        }
