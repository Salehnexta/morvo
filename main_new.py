"""
Morvo AI - مساعد التسويق الذكي
Main FastAPI Application
"""

import logging
import os
from datetime import datetime
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import configurations and managers
from config import APP_VERSION, DEBUG
from websocket_manager import handle_websocket_connection, manager
from models import AwarioWebhookData

# Import route modules
from routes.chat import router as chat_router
from routes.analytics import router as analytics_router
from routes.social import router as social_router
from routes.seo import router as seo_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة حياة التطبيق"""
    logger.info("🚀 بدء تشغيل Morvo AI...")
    yield
    logger.info("🛑 إيقاف Morvo AI...")

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Morvo AI - مساعد التسويق الذكي",
    description="نظام ذكي متكامل للتسويق الرقمي يضم 5 وكلاء متخصصين",
    version=APP_VERSION,
    lifespan=lifespan
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل المسارات
app.include_router(chat_router)
app.include_router(analytics_router)
app.include_router(social_router)
app.include_router(seo_router)

# المسارات الأساسية
@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {
        "message": "مرحباً بك في Morvo AI - مساعد التسويق الذكي",
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": APP_VERSION,
        "agents": [
            {"id": "M1", "name": "محلل استراتيجي متقدم", "status": "active"},
            {"id": "M2", "name": "مراقب وسائل التواصل", "status": "active"},
            {"id": "M3", "name": "محسن الحملات", "status": "active"},
            {"id": "M4", "name": "استراتيجي المحتوى", "status": "active"},
            {"id": "M5", "name": "محلل البيانات", "status": "active"}
        ],
        "websocket_connections": manager.get_connection_count()
    }

# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """نقطة اتصال WebSocket"""
    await handle_websocket_connection(websocket, user_id)

# Webhook endpoints
@app.post("/webhooks/awario")
async def awario_webhook(payload: AwarioWebhookData):
    """استقبال webhook من Awario للإشارات الجديدة"""
    try:
        # بث الإشارة الجديدة لجميع المتصلين
        await manager.broadcast({
            "type": "new_mention",
            "source": "awario",
            "data": {
                "mention_id": payload.mention_id,
                "content": payload.content,
                "source": payload.source,
                "sentiment": payload.sentiment,
                "author": payload.author,
                "url": payload.url,
                "timestamp": payload.timestamp.isoformat()
            }
        })
        
        return {"status": "received", "message": "تم استقبال الإشارة وبثها"}
        
    except Exception as e:
        logger.error(f"خطأ في webhook Awario: {e}")
        raise HTTPException(status_code=500, detail="خطأ في معالجة webhook")

# تشغيل التطبيق
if __name__ == "__main__":
    import uvicorn
    import os
    
    # استخدام PORT من متغيرات البيئة (Railway) أو 8001 محلياً
    port = int(os.getenv("PORT", 8001))
    
    logger.info(f"🚀 تشغيل Morvo AI على المنفذ {port}")
    uvicorn.run(
        "main_new:app",
        host="0.0.0.0",
        port=port,
        reload=DEBUG,
        log_level="info"
    )
