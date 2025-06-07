"""
SEO Routes for Morvo AI
مسارات السيو لـ Morvo AI
"""

import logging
import httpx
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import PROVIDERS_AVAILABLE, RAPIDAPI_KEY, RAPIDAPI_SEO_HOST, RAPIDAPI_SEO_BASE_URL

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/seo", tags=["seo"])

# SEO Audit Request Model
class SEOAuditRequest(BaseModel):
    website: str
    detailed: Optional[bool] = False

# Import providers manager when available
try:
    from providers import ProvidersManager
    providers_manager = ProvidersManager()
except ImportError:
    providers_manager = None

@router.post("/audit")
async def audit_website(request: SEOAuditRequest):
    """تدقيق وتحليل الموقع للسيو باستخدام RapidAPI"""
    
    if not RAPIDAPI_KEY:
        raise HTTPException(
            status_code=500, 
            detail="مفتاح RapidAPI غير محدد. يرجى إضافة RAPIDAPI_KEY في متغيرات البيئة"
        )
    
    try:
        # Prepare RapidAPI request
        url = f"{RAPIDAPI_SEO_BASE_URL}/onpagepro.php"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_SEO_HOST
        }
        
        # Query parameters as shown in the API documentation
        params = {
            "website": request.website
        }
        
        # Make async API request using httpx
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"خطأ في API: {response.status_code} - {response.text}"
            )
        
        # Parse the response
        audit_data = response.json()
        
        # Return structured response
        return {
            "status": "success",
            "website": request.website,
            "audit_results": audit_data,
            "analyzed_at": datetime.now().isoformat(),
            "provider": "RapidAPI SEO Audit Pro",
            "api_response_time": f"{response.elapsed.total_seconds():.2f}s"
        }
        
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="انتهت مهلة الاتصال بـ API")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="فشل الاتصال بخدمة التدقيق")
    except httpx.HTTPError as e:
        logger.error(f"خطأ في طلب API: {e}")
        raise HTTPException(status_code=500, detail="خطأ في خدمة التدقيق")
    except Exception as e:
        logger.error(f"خطأ عام في تدقيق الموقع: {e}")
        raise HTTPException(status_code=500, detail="فشل في تحليل الموقع")

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
