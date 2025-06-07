"""
Configuration for Morvo AI
إعدادات Morvo AI

Enhanced configuration for MCP (Model Context Protocol) and A2A (Agent-to-Agent) Integration
with Supabase, Git, Security, and advanced features
"""

import os
from typing import Dict, List

# Core Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Supabase Configuration (Primary Database)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Auto-generate Supabase DATABASE_URL if Supabase is configured
if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    # Extract project reference from Supabase URL
    supabase_ref = SUPABASE_URL.replace("https://", "").replace(".supabase.co", "")
    SUPABASE_DATABASE_URL = f"postgresql://postgres:{SUPABASE_SERVICE_ROLE_KEY}@db.{supabase_ref}.supabase.co:5432/postgres"
else:
    SUPABASE_DATABASE_URL = None

# Database Configuration (Fallback to Railway/Local if Supabase not available)
DATABASE_URL = os.getenv("DATABASE_URL") or SUPABASE_DATABASE_URL
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))
DATABASE_NAME = os.getenv("DATABASE_NAME", "morvo_ai")
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Redis Configuration for Caching and Sessions
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Security and Authentication
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "morvo-ai-enhanced-secret-key-2025")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# MCP (Model Context Protocol) Configuration
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 3000))
MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "streamable-http")
MCP_MAX_CONNECTIONS = int(os.getenv("MCP_MAX_CONNECTIONS", 100))
MCP_TIMEOUT = int(os.getenv("MCP_TIMEOUT", 30))

# A2A (Agent-to-Agent) Protocol Configuration
A2A_NETWORK_ID = os.getenv("A2A_NETWORK_ID", "morvo-ai-network")
A2A_AUTH_ENABLED = os.getenv("A2A_AUTH_ENABLED", "true").lower() == "true"
A2A_MESSAGE_TTL = int(os.getenv("A2A_MESSAGE_TTL", 3600))  # 1 hour
A2A_MAX_RETRIES = int(os.getenv("A2A_MAX_RETRIES", 3))
A2A_RETRY_DELAY = int(os.getenv("A2A_RETRY_DELAY", 5))  # seconds

# RapidAPI Configuration for SEO Audit
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_SEO_HOST = "website-analyze-and-seo-audit-pro.p.rapidapi.com"
RAPIDAPI_SEO_BASE_URL = f"https://{RAPIDAPI_SEO_HOST}"

# Git Integration Configuration
GIT_REPO_PATH = os.getenv("GIT_REPO_PATH", ".")
GIT_USERNAME = os.getenv("GIT_USERNAME")
GIT_EMAIL = os.getenv("GIT_EMAIL")
GIT_TOKEN = os.getenv("GIT_TOKEN")
GIT_REMOTE_URL = os.getenv("GIT_REMOTE_URL")
GIT_AUTO_COMMIT = os.getenv("GIT_AUTO_COMMIT", "false").lower() == "true"
GIT_AUTO_PUSH = os.getenv("GIT_AUTO_PUSH", "false").lower() == "true"

# File Processing Configuration
UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", "./uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB
ALLOWED_FILE_TYPES = os.getenv("ALLOWED_FILE_TYPES", "pdf,txt,md,docx,png,jpg,jpeg").split(",")

# Marketing providers
SERANKING_API_KEY = os.getenv("SERANKING_API_KEY")
AWARIO_API_KEY = os.getenv("AWARIO_API_KEY")
AWARIO_WEBHOOK_URL = os.getenv("AWARIO_WEBHOOK_URL")
MENTION_API_KEY = os.getenv("MENTION_API_KEY")
MENTION_ACCOUNT_ID = os.getenv("MENTION_ACCOUNT_ID")

# Social Media API Keys
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

# Analytics API Keys
GOOGLE_ANALYTICS_CREDENTIALS = os.getenv("GOOGLE_ANALYTICS_CREDENTIALS")
GOOGLE_ANALYTICS_PROPERTY_ID = os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID")
SEMRUSH_API_KEY = os.getenv("SEMRUSH_API_KEY")
AHREFS_API_KEY = os.getenv("AHREFS_API_KEY")

# App settings
APP_VERSION = "2.0.0"
APP_NAME = "Morvo AI Enhanced"
APP_DESCRIPTION = "Enhanced AI Marketing Platform with MCP and A2A Protocols"
PORT = int(os.getenv("PORT", 8001))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Performance and Scaling
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", 60))

# Enhanced Agent configurations with MCP capabilities
AGENTS_CONFIG = [
    {
        "id": "M1",
        "name": "محلل استراتيجي متقدم",
        "role": "Strategic Analyst",
        "goal": "تحليل السوق والمنافسين وتقديم توصيات استراتيجية شاملة",
        "backstory": "خبير في التحليل الاستراتيجي مع 15+ سنة خبرة في الأسواق العربية",
        "keywords": ["استراتيجية", "تحليل سوق", "منافسين", "تموضع", "خطة"],
        "capabilities": ["market_analysis", "competitor_research", "strategic_planning"],
        "mcp_resources": ["schema://agents/enhanced", "data://supabase/projects"],
        "a2a_endpoints": ["analysis", "research", "planning"]
    },
    {
        "id": "M2", 
        "name": "مراقب وسائل التواصل الاجتماعي",
        "role": "Social Media Monitor",
        "goal": "مراقبة وتحليل المنصات الاجتماعية وتتبع التفاعل",
        "backstory": "متخصص في إدارة وسائل التواصل الاجتماعي مع خبرة في الأسواق العربية",
        "keywords": ["سوشيال", "تواصل", "فيسبوك", "انستغرام", "تويتر", "لينكد"],
        "capabilities": ["social_monitoring", "sentiment_analysis", "engagement_tracking"],
        "mcp_resources": ["data://social/mentions", "analytics://social/metrics"],
        "a2a_endpoints": ["monitoring", "sentiment", "engagement"]
    },
    {
        "id": "M3",
        "name": "محسن الحملات التسويقية", 
        "role": "Campaign Optimizer",
        "goal": "تحليل وتحسين أداء الحملات التسويقية وعائد الاستثمار",
        "backstory": "خبير في تحسين الحملات الرقمية مع تركيز على ROI والنتائج القابلة للقياس",
        "keywords": ["حملة", "إعلان", "تحسين", "roi", "ميزانية", "أداء"],
        "capabilities": ["campaign_optimization", "roi_analysis", "budget_management"],
        "mcp_resources": ["analytics://campaigns", "data://roi/metrics"],
        "a2a_endpoints": ["optimization", "roi", "budget"]
    },
    {
        "id": "M4",
        "name": "استراتيجي المحتوى الإبداعي",
        "role": "Content Strategist", 
        "goal": "تطوير استراتيجيات المحتوى والتقويم الإبداعي",
        "backstory": "كاتب محتوى مبدع مع خبرة في استراتيجيات المحتوى للعلامات التجارية العربية",
        "keywords": ["محتوى", "كتابة", "منشور", "مقال", "فيديو", "تقويم"],
        "capabilities": ["content_strategy", "creative_planning", "editorial_calendar"],
        "mcp_resources": ["content://templates", "planning://calendar"],
        "a2a_endpoints": ["content", "creative", "calendar"]
    },
    {
        "id": "M5",
        "name": "محلل البيانات التسويقية المتقدم",
        "role": "Data Analyst",
        "goal": "تحويل البيانات إلى رؤى قابلة للتنفيذ وتوصيات مبنية على البيانات",
        "backstory": "محلل بيانات متقدم مع خبرة في تحليل البيانات التسويقية الضخمة",
        "keywords": ["بيانات", "تحليل", "إحصائيات", "أرقام", "تقرير", "رؤى"],
        "capabilities": ["data_analysis", "predictive_modeling", "insights_generation"],
        "mcp_resources": ["analytics://data", "insights://predictive"],
        "a2a_endpoints": ["analysis", "modeling", "insights"]
    }
]

# Enhanced Providers configuration with MCP integration
PROVIDERS_CONFIG = {
    "se_ranking": {
        "name": "SE Ranking",
        "plan": "Business Plan",
        "cost": "$378/month",
        "features": ["2,500 keywords tracking", "competitor analysis", "SERP data"],
        "mcp_enabled": True,
        "api_endpoints": ["keywords", "competitors", "serp"],
        "webhook_support": True
    },
    "awario": {
        "name": "Awario", 
        "plan": "Enterprise",
        "cost": "$399/month",
        "features": ["100 topics", "1M mentions/month", "webhook support"],
        "mcp_enabled": True,
        "api_endpoints": ["mentions", "sentiment", "reach"],
        "webhook_support": True
    },
    "mention": {
        "name": "Mention",
        "plan": "Pro Plus", 
        "cost": "$179/month",
        "features": ["15 social platforms", "unified inbox", "auto-reply"],
        "mcp_enabled": True,
        "api_endpoints": ["mentions", "inbox", "analytics"],
        "webhook_support": True
    },
    "supabase": {
        "name": "Supabase",
        "plan": "Pro",
        "cost": "$25/month",
        "features": ["Real-time database", "Authentication", "Storage", "Edge Functions"],
        "mcp_enabled": True,
        "api_endpoints": ["database", "auth", "storage", "functions"],
        "webhook_support": True
    },
    "redis": {
        "name": "Redis Cloud",
        "plan": "Basic",
        "cost": "$5/month", 
        "features": ["Caching", "Session storage", "Message queuing"],
        "mcp_enabled": True,
        "api_endpoints": ["cache", "pubsub", "streams"],
        "webhook_support": False
    }
}

# Enhanced Feature Flags
FEATURES = {
    "mcp_protocol": True,
    "a2a_protocol": True,
    "supabase_integration": True,
    "git_integration": True,
    "advanced_caching": True,
    "real_time_sync": True,
    "webhook_support": True,
    "file_processing": True,
    "social_media_apis": True,
    "analytics_apis": True,
    "predictive_modeling": True,
    "auto_scaling": True,
    "security_monitoring": True,
    "performance_optimization": True
}

# Check if enhanced protocols are available
ENHANCED_PROTOCOLS_AVAILABLE = all([
    OPENAI_API_KEY,
    SUPABASE_URL and SUPABASE_KEY,
    JWT_SECRET_KEY
])

# Check if providers are available
PROVIDERS_AVAILABLE = all([
    SERANKING_API_KEY,
    AWARIO_API_KEY, 
    MENTION_API_KEY
])

# MCP Resource Definitions
MCP_RESOURCES = {
    "agents_schema": "schema://agents/enhanced",
    "supabase_projects": "data://supabase/projects",
    "git_status": "git://repository/status",
    "analytics_data": "analytics://marketing/data",
    "social_mentions": "data://social/mentions",
    "campaign_metrics": "analytics://campaigns/metrics",
    "content_templates": "content://templates/library",
    "performance_insights": "insights://performance/advanced"
}

# A2A Network Configuration
A2A_NETWORK_CONFIG = {
    "network_id": A2A_NETWORK_ID,
    "authentication_required": A2A_AUTH_ENABLED,
    "message_encryption": True,
    "max_message_size": 1048576,  # 1MB
    "supported_protocols": ["HTTP", "WebSocket", "gRPC"],
    "load_balancing": True,
    "failover_enabled": True,
    "monitoring_enabled": True
}

# Security Configuration
SECURITY_CONFIG = {
    "cors_enabled": True,
    "cors_origins": ["*", "http://localhost", "http://localhost:3000", "http://127.0.0.1", "file://"] if DEBUG else ["http://localhost", "http://localhost:3000", "http://127.0.0.1", "file://"],
    "rate_limiting_enabled": True,
    "ip_whitelisting_enabled": False,
    "request_validation": True,
    "response_compression": True,
    "security_headers": True,
    "csrf_protection": True,
    "xss_protection": True
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "default"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "morvo_ai.log",
            "level": "INFO",
            "formatter": "detailed"
        }
    },
    "loggers": {
        "": {
            "level": LOG_LEVEL,
            "handlers": ["console", "file"]
        },
        "mcp": {
            "level": "DEBUG" if DEBUG else "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "a2a": {
            "level": "DEBUG" if DEBUG else "INFO", 
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
}
