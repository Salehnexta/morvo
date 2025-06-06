"""
Analytics Routes for Morvo AI
مسارات التحليلات لـ Morvo AI
"""

import logging
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from models import AnalyticsRequest, AnalysisRequest
from config import PROVIDERS_AVAILABLE, PROVIDERS_CONFIG

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/analytics", tags=["analytics"])

# Import providers manager when available
try:
    from providers import ProvidersManager
    providers_manager = ProvidersManager()
except ImportError:
    providers_manager = None

@router.get("/providers/status")
async def get_providers_status():
    """الحصول على حالة مزودي البيانات التسويقية"""
    return {
        "status": "ready",
        "message": "مزودو البيانات جاهزون للتفعيل الأسبوع القادم",
        "expected_providers": {
            "SE Ranking": "Business Plan ($378/month)",
            "Awario": "Enterprise ($399/month)", 
            "Mention": "Pro Plus ($179/month)"
        },
        "activation_date": "2024-12-14",
        "total_cost": "$956/month",
        "timestamp": datetime.now().isoformat()
    }

@router.post("/comprehensive")
async def comprehensive_analytics(request: AnalysisRequest):
    """تحليل شامل للعلامة التجارية عبر جميع مزودي البيانات"""
    if not PROVIDERS_AVAILABLE:
        return {
            "status": "success",
            "message": f"تحليل شامل لـ '{request.brand}' سيتم تفعيله الأسبوع القادم",
            "brand": request.brand,
            "keywords_count": len(request.keywords),
            "expected_features": [
                "تحليل SEO شامل عبر SE Ranking",
                "مراقبة اجتماعية فورية عبر Awario",
                "تحليل الكلمات المفتاحية",
                "مراقبة المنافسين",
                "تقارير أداء شاملة"
            ],
            "activation_date": "2024-12-14",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        # When providers are available, use real data
        comprehensive_data = await providers_manager.get_comprehensive_analysis(
            brand=request.brand,
            keywords=request.keywords,
            timeframe=request.timeframe,
            competitors=request.competitors
        )
        
        return {
            "status": "success",
            "brand": request.brand,
            "analysis": comprehensive_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"خطأ في التحليل الشامل: {e}")
        raise HTTPException(status_code=500, detail="فشل في جلب التحليل الشامل")
