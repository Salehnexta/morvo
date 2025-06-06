"""
Chat Routes for Morvo AI
مسارات المحادثة لـ Morvo AI
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from models import ChatMessage, ChatResponse
from agents import MorvoAgents

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/chat", tags=["chat"])

# Initialize agents
morvo_agents = MorvoAgents()

@router.post("/message", response_model=ChatResponse)
async def process_chat_message(message: ChatMessage):
    """معالجة رسالة المحادثة"""
    try:
        # معالجة الرسالة عبر الوكلاء
        result = await morvo_agents.process_message(
            content=message.content,
            user_id=message.user_id,
            session_id=message.session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        return ChatResponse(
            content=result["content"],
            agent_used=result["agent_used"],
            intent_detected=result["intent_detected"],
            timestamp=datetime.now(),
            session_id=result["session_id"]
        )
        
    except Exception as e:
        logger.error(f"خطأ في معالجة رسالة المحادثة: {e}")
        raise HTTPException(status_code=500, detail="خطأ في معالجة الرسالة")

@router.get("/agents/status")
async def get_agents_status():
    """الحصول على حالة الوكلاء"""
    try:
        agents_status = morvo_agents.get_agents_status()
        return {
            "status": "active",
            "agents": agents_status,
            "total_agents": len(agents_status),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"خطأ في جلب حالة الوكلاء: {e}")
        raise HTTPException(status_code=500, detail="خطأ في جلب حالة الوكلاء")
