"""
WebSocket Manager for Morvo AI
إدارة WebSocket لـ Morvo AI
"""

import logging
import json
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """مدير اتصالات WebSocket"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str):
        """قبول اتصال WebSocket جديد"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"اتصال WebSocket جديد: {user_id}")
        
        # إرسال رسالة ترحيب
        await self.send_personal_message({
            "type": "connection_established",
            "message": "تم تأسيس الاتصال بنجاح مع Morvo AI",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }, user_id)
        
    def disconnect(self, user_id: str):
        """قطع اتصال WebSocket"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"تم قطع اتصال WebSocket: {user_id}")
            
    async def send_personal_message(self, data: dict, user_id: str):
        """إرسال رسالة شخصية لمستخدم محدد"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(data, ensure_ascii=False))
            except Exception as e:
                logger.error(f"خطأ في إرسال رسالة WebSocket لـ {user_id}: {e}")
                self.disconnect(user_id)
                
    async def broadcast(self, data: dict):
        """بث رسالة لجميع المتصلين"""
        disconnected_users = []
        
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(json.dumps(data, ensure_ascii=False))
            except Exception as e:
                logger.error(f"خطأ في بث رسالة WebSocket لـ {user_id}: {e}")
                disconnected_users.append(user_id)
                
        # إزالة الاتصالات المنقطعة
        for user_id in disconnected_users:
            self.disconnect(user_id)
            
    def get_connection_count(self) -> int:
        """الحصول على عدد الاتصالات النشطة"""
        return len(self.active_connections)
    
    def get_connected_users(self) -> List[str]:
        """الحصول على قائمة المستخدمين المتصلين"""
        return list(self.active_connections.keys())

# إنشاء مثيل مدير الاتصالات
manager = ConnectionManager()

async def handle_websocket_connection(websocket: WebSocket, user_id: str):
    """التعامل مع اتصال WebSocket"""
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # انتظار رسائل من العميل
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # معالجة أنواع مختلفة من الرسائل
            if message_data.get("type") == "ping":
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }, user_id)
                
            elif message_data.get("type") == "status_request":
                await manager.send_personal_message({
                    "type": "status_response",
                    "connected_users": manager.get_connection_count(),
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                }, user_id)
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        logger.info(f"WebSocket connection closed for user: {user_id}")
        
    except Exception as e:
        logger.error(f"خطأ في WebSocket للمستخدم {user_id}: {e}")
        manager.disconnect(user_id)
