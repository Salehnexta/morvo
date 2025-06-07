"""
Morvo AI - مساعد التسويق الذكي
Enhanced Main FastAPI Application with MCP & A2A Protocol Integration
التطبيق الرئيسي المحسن مع تكامل بروتوكولات MCP و A2A
"""

import logging
import os
from datetime import datetime
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import enhanced configurations and managers
from config import (
    APP_VERSION, APP_NAME, APP_DESCRIPTION, DEBUG,
    ENHANCED_PROTOCOLS_AVAILABLE, FEATURES, SECURITY_CONFIG, LOGGING_CONFIG
)
from websocket_manager import handle_websocket_connection, manager
from models import AwarioWebhookData

# Import modular protocols
from protocols import EnhancedProtocolManager

# Import route modules
from routes.chat import router as chat_router
from routes.analytics import router as analytics_router
from routes.social import router as social_router
from routes.seo import router as seo_router

# Configure enhanced logging
import logging.config
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Initialize global protocol manager
protocol_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة حياة التطبيق المحسنة مع بروتوكولات MCP و A2A"""
    global protocol_manager
    
    logger.info("🚀 بدء تشغيل Morvo AI Enhanced...")
    logger.info(f"📦 الإصدار: {APP_VERSION}")
    logger.info(f"🔧 البروتوكولات المتقدمة: {'متاحة' if ENHANCED_PROTOCOLS_AVAILABLE else 'غير متاحة'}")
    
    # Initialize enhanced protocols
    if ENHANCED_PROTOCOLS_AVAILABLE:
        try:
            logger.info("🔄 تهيئة البروتوكولات المحسنة...")
            protocol_manager = EnhancedProtocolManager()
            
            # Startup protocols
            await protocol_manager.startup()
            logger.info("✅ تم تشغيل البروتوكولات المحسنة بنجاح")
            
            # Store in app state for access in routes
            app.state.protocol_manager = protocol_manager
            
        except Exception as e:
            logger.error(f"❌ فشل في تشغيل البروتوكولات: {e}")
            # Continue without enhanced protocols
            app.state.protocol_manager = None
    else:
        logger.warning("⚠️ البروتوكولات المحسنة غير متاحة - متابعة التشغيل في الوضع الأساسي")
        app.state.protocol_manager = None
    
    # Log enabled features
    enabled_features = [feature for feature, enabled in FEATURES.items() if enabled]
    logger.info(f"🎯 الميزات المفعلة: {', '.join(enabled_features)}")
    
    yield
    
    # Shutdown protocols
    logger.info("🛑 إيقاف Morvo AI...")
    if protocol_manager:
        try:
            await protocol_manager.shutdown()
            logger.info("✅ تم إيقاف البروتوكولات بنجاح")
        except Exception as e:
            logger.error(f"❌ خطأ في إيقاف البروتوكولات: {e}")

# إنشاء تطبيق FastAPI محسن
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None
)

# إعداد CORS محسن
cors_origins = SECURITY_CONFIG.get("cors_origins", ["*"]) if SECURITY_CONFIG.get("cors_enabled", True) else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل المسارات
app.include_router(chat_router)
app.include_router(analytics_router)
app.include_router(social_router)
app.include_router(seo_router)

# المسارات الأساسية المحسنة
@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {
        "message": "مرحباً بك في Morvo AI Enhanced - مساعد التسويق الذكي المحسن",
        "version": APP_VERSION,
        "protocols": {
            "mcp": FEATURES.get("mcp_protocol", False),
            "a2a": FEATURES.get("a2a_protocol", False),
            "enhanced_available": ENHANCED_PROTOCOLS_AVAILABLE
        },
        "features": {
            "supabase_integration": FEATURES.get("supabase_integration", False),
            "git_integration": FEATURES.get("git_integration", False),
            "advanced_caching": FEATURES.get("advanced_caching", False),
            "real_time_sync": FEATURES.get("real_time_sync", False)
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "health_detailed": "/health/detailed",
            "protocols": "/protocols/status",
            "mcp_resources": "/mcp/resources",
            "a2a_network": "/a2a/network"
        }
    }

@app.get("/health")
async def health_check():
    """فحص صحة النظام الأساسي"""
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
        "websocket_connections": manager.get_connection_count(),
        "protocols_enhanced": ENHANCED_PROTOCOLS_AVAILABLE
    }

@app.get("/health/detailed")
async def detailed_health_check():
    """فحص صحة النظام المفصل مع البروتوكولات"""
    base_health = {
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
        "websocket_connections": manager.get_connection_count(),
        "features": FEATURES
    }
    
    # Add enhanced protocol health if available
    if hasattr(app.state, 'protocol_manager') and app.state.protocol_manager:
        try:
            protocol_health = await app.state.protocol_manager.health_check()
            base_health["protocols"] = protocol_health
        except Exception as e:
            logger.error(f"خطأ في فحص صحة البروتوكولات: {e}")
            base_health["protocols"] = {"error": str(e)}
    else:
        base_health["protocols"] = {"status": "not_available"}
    
    return base_health

@app.get("/protocols/status")
async def protocols_status():
    """حالة البروتوكولات المحسنة"""
    if not hasattr(app.state, 'protocol_manager') or not app.state.protocol_manager:
        return {"error": "البروتوكولات المحسنة غير متاحة"}
    
    try:
        return await app.state.protocol_manager.health_check()
    except Exception as e:
        logger.error(f"خطأ في جلب حالة البروتوكولات: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/resources")
async def mcp_resources():
    """موارد MCP المتاحة"""
    if not hasattr(app.state, 'protocol_manager') or not app.state.protocol_manager:
        return {"error": "بروتوكول MCP غير متاح"}
    
    try:
        # Get MCP resources from protocol manager
        resources = await app.state.protocol_manager.mcp_server.list_resources()
        return {"resources": resources}
    except Exception as e:
        logger.error(f"خطأ في جلب موارد MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/a2a/network")
async def a2a_network_status():
    """حالة شبكة A2A"""
    if not hasattr(app.state, 'protocol_manager') or not app.state.protocol_manager:
        return {"error": "بروتوكول A2A غير متاح"}
    
    try:
        # Get A2A network status
        agents = list(app.state.protocol_manager.a2a_handler.agents.keys())
        return {
            "network_id": app.state.protocol_manager.a2a_handler.network_id,
            "registered_agents": len(agents),
            "agents": agents,
            "message_queue_size": len(app.state.protocol_manager.a2a_handler.message_queue)
        }
    except Exception as e:
        logger.error(f"خطأ في جلب حالة شبكة A2A: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint محسن
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """نقطة اتصال WebSocket محسنة"""
    await handle_websocket_connection(websocket, user_id)

# Enhanced webhook endpoints
@app.post("/webhooks/awario")
async def awario_webhook(payload: AwarioWebhookData):
    """استقبال webhook من Awario للإشارات الجديدة"""
    try:
        # Store in enhanced protocols if available
        if hasattr(app.state, 'protocol_manager') and app.state.protocol_manager:
            try:
                # Cache the mention data
                await app.state.protocol_manager.redis_client.hset(
                    "mentions:awario",
                    payload.mention_id,
                    {
                        "content": payload.content,
                        "sentiment": payload.sentiment,
                        "timestamp": payload.timestamp.isoformat()
                    }
                )
                logger.info(f"تم حفظ إشارة Awario في التخزين المؤقت: {payload.mention_id}")
            except Exception as e:
                logger.warning(f"فشل في حفظ إشارة Awario: {e}")
        
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

@app.post("/webhooks/mention")
async def mention_webhook(payload: dict):
    """استقبال webhook من Mention"""
    try:
        # Store in enhanced protocols if available
        if hasattr(app.state, 'protocol_manager') and app.state.protocol_manager:
            try:
                mention_id = payload.get("id", "unknown")
                await app.state.protocol_manager.redis_client.hset(
                    "mentions:mention",
                    mention_id,
                    payload
                )
                logger.info(f"تم حفظ إشارة Mention في التخزين المؤقت: {mention_id}")
            except Exception as e:
                logger.warning(f"فشل في حفظ إشارة Mention: {e}")
        
        # Broadcast the new mention
        await manager.broadcast({
            "type": "new_mention",
            "source": "mention",
            "data": payload
        })
        
        return {"status": "received", "message": "تم استقبال إشارة Mention"}
        
    except Exception as e:
        logger.error(f"خطأ في webhook Mention: {e}")
        raise HTTPException(status_code=500, detail="خطأ في معالجة webhook")

# تشغيل التطبيق
if __name__ == "__main__":
    import uvicorn
    
    # استخدام PORT من متغيرات البيئة (Railway) أو 8001 محلياً
    port = int(os.getenv("PORT", 8001))
    
    logger.info(f"🚀 تشغيل Morvo AI Enhanced على المنفذ {port}")
    logger.info(f"🔧 البروتوكولات المحسنة: {'مفعلة' if ENHANCED_PROTOCOLS_AVAILABLE else 'معطلة'}")
    
    uvicorn.run(
        "main_new:app",
        host="0.0.0.0",
        port=port,
        reload=DEBUG,
        log_level="info" if not DEBUG else "debug"
    )
