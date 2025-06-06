"""
Social Media Routes for Morvo AI
مسارات وسائل التواصل لـ Morvo AI
"""

import logging
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from models import SocialPostRequest
from config import PROVIDERS_AVAILABLE

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/social", tags=["social"])

# Import providers manager when available
try:
    from providers import ProvidersManager
    providers_manager = ProvidersManager()
except ImportError:
    providers_manager = None

@router.post("/schedule-post")
async def schedule_social_post(request: SocialPostRequest):
    """جدولة منشور عبر منصات متعددة"""
    if not PROVIDERS_AVAILABLE:
        return {
            "status": "success",
            "message": f"جدولة المنشور عبر {len(request.platforms)} منصات سيتم تفعيلها الأسبوع القادم",
            "platforms_count": len(request.platforms),
            "platforms": request.platforms,
            "features_coming": [
                "نشر موحد عبر 15 منصة",
                "جدولة ذكية بأفضل أوقات التفاعل", 
                "تحسين المحتوى لكل منصة",
                "تتبع أداء المنشورات",
                "تحليل ROI للمنشورات"
            ],
            "provider": "Mention Pro Plus",
            "activation_date": "2024-12-14",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        # When providers are available, use real scheduling
        result = await providers_manager.mention.schedule_post(
            content=request.content,
            platforms=request.platforms,
            schedule_time=request.schedule_time,
            media_urls=request.media_urls
        )
        
        return {
            "status": "scheduled",
            "post_id": result.get("post_id"),
            "platforms": request.platforms,
            "schedule_time": request.schedule_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"خطأ في جدولة المنشور: {e}")
        raise HTTPException(status_code=500, detail="فشل في جدولة المنشور")

@router.get("/inbox")
async def get_social_inbox():
    """الحصول على صندوق الوارد الموحد"""
    if not PROVIDERS_AVAILABLE:
        return {
            "status": "success",
            "message": "صندوق الوارد الموحد سيتم تفعيله الأسبوع القادم",
            "features_coming": [
                "إدارة موحدة للتفاعلات",
                "ردود تلقائية ذكية باللغة العربية",
                "تصنيف الرسائل حسب الأولوية",
                "تحليل مشاعر التفاعلات",
                "إحصائيات التفاعل المفصلة"
            ],
            "provider": "Mention Pro Plus + Awario Enterprise",
            "activation_date": "2024-12-14",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        # When providers are available, fetch real inbox data
        inbox_data = await providers_manager.mention.get_inbox()
        mentions_data = await providers_manager.awario.get_mentions()
        
        return {
            "status": "success",
            "inbox": inbox_data,
            "mentions": mentions_data,
            "total_items": len(inbox_data) + len(mentions_data),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"خطأ في جلب صندوق الوارد: {e}")
        raise HTTPException(status_code=500, detail="فشل في جلب صندوق الوارد")
