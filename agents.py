"""
Enhanced Morvo AI Companion with MCP & A2A Protocol Integration
رفيق Morvo AI المحسن مع دمج بروتوكولات MCP و A2A
"""

import asyncio
import logging
import json
import httpx
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from crewai import Agent, Task, Crew
from config import AGENTS_CONFIG

# Supabase integration for MCP
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️ Supabase client not available, using fallback mode")

logger = logging.getLogger(__name__)

class UnifiedMorvoCompanion:
    """رفيق مورفو الموحد - مساعد تسويق ذكي واحد"""
    
    def __init__(self):
        self.system_prompt = None
        self.supabase_client = None
        self._initialize_companion()
    
    def _initialize_companion(self):
        """تهيئة رفيق مورفو الموحد"""
        try:
            if SUPABASE_AVAILABLE:
                url = os.getenv('SUPABASE_URL')
                key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
                if url and key:
                    self.supabase_client = create_client(url, key)
                    logger.info("✅ Unified Morvo Companion initialized")
            
            # Load system prompt from database or use fallback
            asyncio.create_task(self._load_system_prompt())
            
        except Exception as e:
            logger.error(f"❌ Error initializing Morvo Companion: {e}")
    
    async def _load_system_prompt(self):
        """تحميل System Prompt من قاعدة البيانات"""
        try:
            if self.supabase_client:
                response = self.supabase_client.table("prompts").select("content").eq("name", "morvo_unified_companion").eq("is_active", True).execute()
                if response.data:
                    self.system_prompt = response.data[0]['content']
                    logger.info("✅ System prompt loaded from database")
                    return
        except Exception as e:
            logger.error(f"❌ Error loading system prompt: {e}")
        
        # Fallback system prompt
        self.system_prompt = """أنت «مورفو» – رفيق تسويق ذكي واحد.
• تحدُّث بالعربية الفصحى بلمسة خليجية ودودة.
• وظيفتك تبسيط التسويق: تحليل SEO، أفكار محتوى، حملات، تتبّع ROI.
• لا تذكر أي لوحة تحكّم أو جداول معقّدة؛ كل شيء يتمّ داخل المحادثة.
• جمَل قصيرة، أفعال مباشرة، إيموجي واحد كحدّ أقصى.
• لا تتجاوز 300 كلمة في أي ردّ."""
    
    async def process_message(self, user_id: str, message: str, filters: Dict = None) -> Dict[str, Any]:
        """معالجة الرسالة مع رفيق مورفو الموحد"""
        logger.info(f"🤖 Processing message with unified Morvo companion for user: {user_id}")
        
        try:
            # Load MCP connector for user context
            from mcp_connector import get_mcp_connector
            mcp_connector = get_mcp_connector()
            
            # Get user context via MCP
            user_context = await mcp_connector.get_user_data(user_id)
            
            # Build unified context for Morvo
            context_prompt = await self._build_unified_context(user_context, message)
            
            # Create unified Morvo agent
            morvo_agent = Agent(
                role="مورفو - رفيق التسويق الذكي",
                goal="تبسيط التسويق وتحقيق أهداف العميل بطريقة محادثية ودودة",
                backstory=self.system_prompt or "رفيق تسويق ذكي يساعد في جميع جوانب التسويق الرقمي",
                verbose=False,
                allow_delegation=False
            )
            
            # Create task for Morvo
            task = Task(
                description=f"""
                تعامل مع هذا الطلب من العميل: {message}
                
                السياق المتاح:
                {context_prompt}
                
                التعليمات:
                - رد بشكل مباشر ومفيد
                - لا تتجاوز 300 كلمة
                - استخدم إيموجي واحد فقط
                - ركز على النتائج والأرقام
                - اقترح خطوة عملية واحدة
                """,
                agent=morvo_agent,
                expected_output="رد مفيد ومباشر يحل مشكلة العميل أو يجيب على سؤاله"
            )
            
            # Execute with Morvo
            crew = Crew(
                agents=[morvo_agent],
                tasks=[task],
                verbose=False
            )
            
            # Process the request
            result = crew.kickoff()
            response_content = str(result) if result else "عذراً، لم أتمكن من معالجة طلبك في الوقت الحالي."
            
            # Save conversation via MCP
            await mcp_connector.save_conversation(
                user_id=user_id,
                content=message,
                response=response_content,
                context=user_context
            )
            
            return {
                "response": response_content,
                "companion": "مورفو",
                "user_context": user_context,
                "mcp_enabled": user_context.get('mcp_enabled', False),
                "conversation_saved": True
            }
            
        except Exception as e:
            logger.error(f"❌ Error in unified Morvo processing: {e}")
            return {
                "response": f"عذراً، حدث خطأ تقني. دعني أساعدك بطريقة أخرى. 🤖",
                "error": str(e),
                "mcp_enabled": False
            }
    
    async def _build_unified_context(self, user_context: Dict, message: str) -> str:
        """بناء السياق الموحد لمورفو"""
        context_parts = []
        
        # User profile context
        if user_context.get('profile'):
            profile = user_context['profile']
            context_parts.append(f"العميل: {profile.get('full_name', 'غير محدد')}")
        
        # Business context
        if user_context.get('campaigns'):
            campaigns_count = len(user_context['campaigns'])
            context_parts.append(f"الحملات النشطة: {campaigns_count}")
        
        # Analytics context
        if user_context.get('analytics'):
            analytics_count = len(user_context['analytics'])
            context_parts.append(f"نقاط البيانات: {analytics_count}")
        
        return "\n".join(context_parts) if context_parts else "لا توجد بيانات إضافية متاحة"
    
    def get_companion_status(self) -> Dict[str, Any]:
        """حالة رفيق مورفو"""
        return {
            "companion_name": "مورفو",
            "status": "active",
            "system_prompt_loaded": bool(self.system_prompt),
            "supabase_connected": bool(self.supabase_client),
            "capabilities": [
                "تحليل SEO",
                "إنشاء محتوى",
                "إدارة حملات",
                "تتبع ROI",
                "تحليل البيانات"
            ]
        }

# For backward compatibility with existing code
class EnhancedMorvoAgents:
    """Wrapper class for backward compatibility"""
    
    def __init__(self):
        self.morvo_companion = UnifiedMorvoCompanion()
        logger.info("🤖 Enhanced Morvo Agents initialized with unified companion")
    
    async def process_message(self, user_id: str, message: str, filters: Dict = None) -> Dict[str, Any]:
        """Process message using unified companion"""
        return await self.morvo_companion.process_message(user_id, message, filters)
    
    def get_agents_status(self) -> List[Dict[str, Any]]:
        """Get status as single companion"""
        companion_status = self.morvo_companion.get_companion_status()
        return [companion_status]  # Return as list for compatibility

# Legacy class for backward compatibility
class MorvoAgents:
    """Legacy wrapper - redirects to unified companion"""
    
    def __init__(self):
        self.enhanced_agents = EnhancedMorvoAgents()
        logger.info("🔄 Legacy MorvoAgents redirecting to unified companion")
    
    async def process_message(self, user_id: str, message: str) -> Dict[str, Any]:
        return await self.enhanced_agents.process_message(user_id, message)
    
    def get_agents_status(self) -> List[Dict[str, Any]]:
        return self.enhanced_agents.get_agents_status()
