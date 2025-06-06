"""
Configuration for Morvo AI
إعدادات Morvo AI
"""

import os
from typing import Dict, List

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Marketing providers
SERANKING_API_KEY = os.getenv("SERANKING_API_KEY")
AWARIO_API_KEY = os.getenv("AWARIO_API_KEY")
AWARIO_WEBHOOK_URL = os.getenv("AWARIO_WEBHOOK_URL")
MENTION_API_KEY = os.getenv("MENTION_API_KEY")
MENTION_ACCOUNT_ID = os.getenv("MENTION_ACCOUNT_ID")

# App settings
APP_VERSION = "2.0"
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Agent configurations
AGENTS_CONFIG = [
    {
        "id": "M1",
        "name": "محلل استراتيجي متقدم",
        "role": "Strategic Analyst",
        "goal": "تحليل السوق والمنافسين وتقديم توصيات استراتيجية شاملة",
        "backstory": "خبير في التحليل الاستراتيجي مع 15+ سنة خبرة في الأسواق العربية",
        "keywords": ["استراتيجية", "تحليل سوق", "منافسين", "تموضع", "خطة"]
    },
    {
        "id": "M2", 
        "name": "مراقب وسائل التواصل الاجتماعي",
        "role": "Social Media Monitor",
        "goal": "مراقبة وتحليل المنصات الاجتماعية وتتبع التفاعل",
        "backstory": "متخصص في إدارة وسائل التواصل الاجتماعي مع خبرة في الأسواق العربية",
        "keywords": ["سوشيال", "تواصل", "فيسبوك", "انستغرام", "تويتر", "لينكد"]
    },
    {
        "id": "M3",
        "name": "محسن الحملات التسويقية", 
        "role": "Campaign Optimizer",
        "goal": "تحليل وتحسين أداء الحملات التسويقية وعائد الاستثمار",
        "backstory": "خبير في تحسين الحملات الرقمية مع تركيز على ROI والنتائج القابلة للقياس",
        "keywords": ["حملة", "إعلان", "تحسين", "roi", "ميزانية", "أداء"]
    },
    {
        "id": "M4",
        "name": "استراتيجي المحتوى الإبداعي",
        "role": "Content Strategist", 
        "goal": "تطوير استراتيجيات المحتوى والتقويم الإبداعي",
        "backstory": "كاتب محتوى مبدع مع خبرة في استراتيجيات المحتوى للعلامات التجارية العربية",
        "keywords": ["محتوى", "كتابة", "منشور", "مقال", "فيديو", "تقويم"]
    },
    {
        "id": "M5",
        "name": "محلل البيانات التسويقية المتقدم",
        "role": "Data Analyst",
        "goal": "تحويل البيانات إلى رؤى قابلة للتنفيذ وتوصيات مبنية على البيانات",
        "backstory": "محلل بيانات متقدم مع خبرة في تحليل البيانات التسويقية الضخمة",
        "keywords": ["بيانات", "تحليل", "إحصائيات", "أرقام", "تقرير", "رؤى"]
    }
]

# Providers configuration
PROVIDERS_CONFIG = {
    "se_ranking": {
        "name": "SE Ranking",
        "plan": "Business Plan",
        "cost": "$378/month",
        "features": ["2,500 keywords tracking", "competitor analysis", "SERP data"]
    },
    "awario": {
        "name": "Awario", 
        "plan": "Enterprise",
        "cost": "$399/month",
        "features": ["100 topics", "1M mentions/month", "webhook support"]
    },
    "mention": {
        "name": "Mention",
        "plan": "Pro Plus", 
        "cost": "$179/month",
        "features": ["15 social platforms", "unified inbox", "auto-reply"]
    }
}

# Check if providers are available
PROVIDERS_AVAILABLE = all([
    SERANKING_API_KEY,
    AWARIO_API_KEY, 
    MENTION_API_KEY
])
