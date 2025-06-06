"""
SEO Routes for Morvo AI
مسارات السيو لـ Morvo AI
"""

import logging
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from config import PROVIDERS_AVAILABLE

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/seo", tags=["seo"])

# Import providers manager when available
try:
    from providers import ProvidersManager
    providers_manager = ProvidersManager()
except ImportError:
    providers_manager = None

@router.post("/keywords")
async def analyze_keywords(keywords: List[str]):
    """تحليل الكلمات المفتاحية عبر SE Ranking"""
    if not PROVIDERS_AVAILABLE:
        return {
            "status": "success", 
            "message": f"تحليل {len(keywords)} كلمة مفتاحية سيتم تفعيله الأسبوع القادم",
            "keywords_count": len(keywords),
            "features_coming": [
                "تتبع ترتيب الكلمات المفتاحية",
                "تحليل صعوبة الكلمات",
                "اقتراحات كلمات جديدة",
                "تحليل المنافسين للكلمات",
                "تقارير أداء مفصلة"
            ],
            "provider": "SE Ranking Business Plan",
            "activation_date": "2024-12-14",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        # When providers are available, use real keyword analysis
        keyword_data = await providers_manager.seranking.get_keyword_data(keywords)
        return {
            "status": "success", 
            "keyword_analysis": keyword_data,
            "keywords_analyzed": len(keywords),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"خطأ في تحليل الكلمات المفتاحية: {e}")
        raise HTTPException(status_code=500, detail="فشل في تحليل الكلمات المفتاحية")

@router.get("/competitors/{domain}")
async def analyze_competitors(domain: str):
    """تحليل المنافسين لنطاق معين"""
    if not PROVIDERS_AVAILABLE:
        return {
            "status": "preparing",
            "message": f"تحليل المنافسين لـ {domain} سيتم تفعيله الأسبوع القادم",
            "domain": domain,
            "features_coming": [
                "تحليل أفضل الكلمات المفتاحية للمنافسين",
                "مقارنة الأداء العام",
                "اكتشاف فرص جديدة",
                "تتبع تغييرات المنافسين"
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        # When providers are available, use real competitor analysis
        competitor_data = await providers_manager.seranking.get_competitor_analysis(domain)
        return {
            "status": "success",
            "domain": domain,
            "competitor_analysis": competitor_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"خطأ في تحليل المنافسين: {e}")
        raise HTTPException(status_code=500, detail="فشل في تحليل المنافسين")
