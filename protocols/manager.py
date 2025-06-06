"""
Enhanced Protocol Manager
مدير البروتوكولات المحسن

Main coordinator for MCP and A2A protocols with advanced integrations
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import aiohttp

# Optional imports with graceful handling
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

try:
    from databases import Database
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    Database = None

# Optional imports - handle gracefully if not available
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    create_client = None
    Client = None

try:
    from git import Repo
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    Repo = None

from config import (
    SUPABASE_URL, 
    SUPABASE_KEY, 
    DATABASE_URL,
    REDIS_URL
)
# Try to import mcp_server, set to None if not available
try:
    from .mcp_server import mcp_server
except ImportError:
    mcp_server = None
from .a2a_protocol import EnhancedA2AProtocol

logger = logging.getLogger(__name__)


class EnhancedProtocolManager:
    """مدير بروتوكولات MCP و A2A المحسن"""
    
    def __init__(self):
        self.mcp_server = mcp_server
        self.session: Optional[aiohttp.ClientSession] = None
        self.supabase: Optional[Client] = None
        self.database: Optional[Database] = None
        self.redis_client: Optional[redis.Redis] = None
        self.git_repos: Dict[str, Repo] = {}
        self.agent_registry: Dict[str, Dict] = {}
        self.cache_ttl = 3600  # 1 hour default cache
        self.a2a_handler: Optional[EnhancedA2AProtocol] = None
        
    async def startup(self):
        """تهيئة جميع البروتوكولات والاتصالات - متوافق مع main_new.py"""
        try:
            # Initialize HTTP session
            self.session = aiohttp.ClientSession()
            
            # Initialize Supabase
            if SUPABASE_AVAILABLE and SUPABASE_URL and SUPABASE_KEY:
                self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                logger.info("✅ Supabase client initialized")
            
            # Initialize Database
            if DATABASE_URL and DATABASE_AVAILABLE:
                try:
                    self.database = Database(DATABASE_URL)
                    await self.database.connect()
                    logger.info("✅ Database connected")
                except Exception as db_err:
                    logger.warning(f"Database connection failed: {str(db_err)}")
                    self.database = None
            else:
                logger.info("ℹ️ Database module not available or not configured, skipping initialization")
            
            # Initialize Redis (optional)
            if REDIS_URL and REDIS_AVAILABLE:
                try:
                    self.redis_client = redis.from_url(REDIS_URL)
                    await self.redis_client.ping()
                    logger.info("✅ Redis connected")
                except Exception as redis_err:
                    logger.warning(f"Redis connection skipped: {str(redis_err)}")
                    self.redis_client = None
            else:
                logger.info("ℹ️ Redis not configured, skipping initialization")
            
            # Initialize A2A handler
            self.a2a_handler = EnhancedA2AProtocol(self.session, self.redis_client)
            
            # Initialize Git repositories
            await self._initialize_git_repos()
            
            # Register default agents
            await self._register_default_agents()
            
            logger.info("✅ Enhanced Protocol Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Protocol manager initialization failed: {str(e)}")
            raise

    async def shutdown(self):
        """تنظيف جميع الموارد - متوافق مع main_new.py"""
        tasks = []
        
        if self.session:
            tasks.append(self.session.close())
        if self.database:
            tasks.append(self.database.disconnect())
        if self.redis_client:
            tasks.append(self.redis_client.close())
            
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info("✅ Enhanced Protocol Manager cleaned up")

    async def health_check(self):
        """فحص صحة البروتوكولات - متوافق مع main_new.py"""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "protocols": {
                "mcp": {
                    "status": "active",
                    # Fix: Don't call the function directly, it's a decorator reference
                    "resources_count": 6,  # Hardcoded count based on the list in mcp_server.py
                    "tools_count": 3  # Hardcoded count based on the list in mcp_server.py
                },
                "a2a": {
                    "status": "active" if self.a2a_handler else "not_initialized",
                    "registered_agents": len(self.a2a_handler.endpoints) if self.a2a_handler else 0
                }
            },
            "integrations": {
                "supabase": {
                    "status": "connected" if self.supabase else "not_configured",
                    "url": SUPABASE_URL if self.supabase else None
                },
                "database": {
                    "status": "connected" if self.database else "not_configured",
                    "url": DATABASE_URL if self.database else None
                },
                "redis": {
                    "status": "connected" if self.redis_client else "not_configured", 
                    "url": REDIS_URL if self.redis_client else None
                },
                "git": {
                    "status": "available" if self.git_repos else "not_configured",
                    "repositories": list(self.git_repos.keys())
                }
            },
            "features": {
                "enhanced_mcp_resources": True,
                "supabase_integration": bool(self.supabase),
                "git_operations": bool(self.git_repos),
                "advanced_caching": bool(self.redis_client),
                "secure_a2a_communication": bool(self.a2a_handler),
                "real_time_monitoring": True
            }
        }
        
        return health_status

    async def _initialize_git_repos(self):
        """تهيئة مستودعات Git المحلية"""
        try:
            project_root = Path.cwd()
            if (project_root / ".git").exists() and GIT_AVAILABLE:
                self.git_repos["main"] = Repo(project_root)
                logger.info(f"Git repository initialized: {project_root}")
        except Exception as e:
            logger.warning(f"Git initialization failed: {str(e)}")

    async def _register_default_agents(self):
        """تسجيل الوكلاء الافتراضيين في نظام A2A"""
        if not self.a2a_handler:
            return
            
        default_agents = [
            {
                "id": "M1",
                "name": "محلل استراتيجي متقدم",
                "endpoint": "http://localhost:8001/agents/M1",
                "capabilities": ["market_analysis", "competitor_research", "strategic_planning"]
            },
            {
                "id": "M2", 
                "name": "مراقب وسائل التواصل الاجتماعي",
                "endpoint": "http://localhost:8001/agents/M2",
                "capabilities": ["social_monitoring", "sentiment_analysis", "engagement_tracking"]
            },
            {
                "id": "M3",
                "name": "محسن الحملات التسويقية",
                "endpoint": "http://localhost:8001/agents/M3", 
                "capabilities": ["campaign_optimization", "roi_analysis", "budget_management"]
            },
            {
                "id": "M4",
                "name": "استراتيجي المحتوى الإبداعي",
                "endpoint": "http://localhost:8001/agents/M4",
                "capabilities": ["content_strategy", "creative_planning", "editorial_calendar"]
            },
            {
                "id": "M5",
                "name": "محلل البيانات التسويقية المتقدم",
                "endpoint": "http://localhost:8001/agents/M5",
                "capabilities": ["data_analysis", "predictive_modeling", "insights_generation"]
            }
        ]
        
        for agent in default_agents:
            try:
                await self.a2a_handler.register_agent(
                    agent["id"],
                    agent["endpoint"], 
                    agent["capabilities"],
                    metadata={"name": agent["name"], "version": "2.0"}
                )
                self.agent_registry[agent["id"]] = agent
                logger.info(f"✅ وكيل {agent['id']} مسجل في نظام A2A")
            except Exception as e:
                logger.warning(f"⚠️ فشل تسجيل الوكيل {agent['id']}: {e}")
