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
        self.system_prompt = """أنت «مورفو» – صديق ومستشار تسويقي ودود وطبيعي في المحادثة.
• تحدُّث كإنسان حقيقي بالعربية الفصحى مع لمسة خليجية دافئة ومريحة.
• تجنب النبرة الرسمية والإحصائيات الكثيرة والمصطلحات التسويقية المعقدة.
• تفاعل بشكل طبيعي وودي كصديق يقدم نصائح مفيدة وبسيطة.
• استخدم كلمات بسيطة وعبارات يومية بدلاً من اللغة الأكاديمية.
• تجنب ذكر النسب والإحصائيات إلا عند الضرورة القصوى.
• اجعل ردودك قصيرة وعفوية، كمحادثة طبيعية بين صديقين.
• استخدم إيموجي واحد فقط لإضفاء لمسة ودية.
• تفاعل بطريقة شخصية تظهر اهتمامك الحقيقي بالمستخدم.
• لا تتجاوز 100-150 كلمة في أي ردّ."""
    
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
                تعامل مع هذا الطلب من الصديق: {message}
                
                السياق المتاح:
                {context_prompt}
                
                التعليمات:
                - تحدث بشكل طبيعي وودي كصديق حقيقي
                - تجنب الإحصائيات والأرقام إلا عند الضرورة
                - استخدم لغة بسيطة وعفوية بعيدة عن الرسمية
                - تجنب المصطلحات التسويقية المعقدة
                - لا تتجاوز 100-150 كلمة
                - استخدم إيموجي واحد فقط إن كان مناسبًا
                - اقترح نصيحة بسيطة بكلمات صديقة
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
        """بناء السياق الموحد الشامل لمورفو - تحليل كامل للبيانات والحملات"""
        context_parts = []
        
        # User profile and business analysis
        if user_context.get('profile'):
            profile = user_context['profile']
            context_parts.append(f"العميل: {profile.get('full_name', 'غير محدد')}")
            context_parts.append(f"النشاط التجاري: {profile.get('business_type', 'غير محدد')}")
            context_parts.append(f"الهدف الرئيسي: {profile.get('business_goal', 'نمو الأعمال')}")
        
        # Marketing campaigns analysis
        if user_context.get('campaigns'):
            campaigns = user_context['campaigns']
            total_campaigns = len(campaigns)
            active_campaigns = len([c for c in campaigns if c.get('status') == 'active'])
            total_budget = sum([float(c.get('budget', 0)) for c in campaigns])
            
            context_parts.append(f"📊 تحليل الحملات:")
            context_parts.append(f"- إجمالي الحملات: {total_campaigns}")
            context_parts.append(f"- الحملات النشطة: {active_campaigns}")
            context_parts.append(f"- إجمالي الميزانية: {total_budget:,.0f} ريال")
            
            # Performance analysis
            if campaigns:
                avg_ctr = sum([float(c.get('ctr', 0)) for c in campaigns]) / len(campaigns)
                avg_conversion = sum([float(c.get('conversion_rate', 0)) for c in campaigns]) / len(campaigns)
                context_parts.append(f"- متوسط CTR: {avg_ctr:.2f}%")
                context_parts.append(f"- متوسط التحويل: {avg_conversion:.2f}%")
        
        # Analytics and KPI analysis
        if user_context.get('analytics'):
            analytics = user_context['analytics']
            total_traffic = sum([int(a.get('page_views', 0)) for a in analytics])
            total_conversions = sum([int(a.get('conversions', 0)) for a in analytics])
            
            context_parts.append(f"📈 تحليل الأداء:")
            context_parts.append(f"- إجمالي الزيارات: {total_traffic:,}")
            context_parts.append(f"- إجمالي التحويلات: {total_conversions:,}")
            
            if total_traffic > 0:
                conversion_rate = (total_conversions / total_traffic) * 100
                context_parts.append(f"- معدل التحويل العام: {conversion_rate:.2f}%")
        
        # Content performance analysis
        if user_context.get('content_performance'):
            content = user_context['content_performance']
            top_content = max(content, key=lambda x: x.get('engagement', 0), default={})
            if top_content:
                context_parts.append(f"🎯 أفضل محتوى: {top_content.get('title', 'غير محدد')}")
                context_parts.append(f"- التفاعل: {top_content.get('engagement', 0):,}")
        
        # SEO analysis
        if user_context.get('seo_data'):
            seo = user_context['seo_data']
            context_parts.append(f"🔍 تحليل SEO:")
            context_parts.append(f"- ترتيب الكلمات المفتاحية: {seo.get('avg_ranking', 'غير متاح')}")
            context_parts.append(f"- نقاط التحسين: {seo.get('improvement_areas', 'تحليل شامل مطلوب')}")
        
        # Smart recommendations based on context
        recommendations = self._generate_smart_recommendations(user_context, message)
        if recommendations:
            context_parts.append(f"💡 توصيات ذكية: {recommendations}")
        
        return '\n'.join(context_parts) if context_parts else 'لا توجد بيانات تحليلية متاحة - سأقدم نصائح عامة مفيدة'
    
    def _generate_smart_recommendations(self, user_context: Dict, message: str) -> str:
        """توليد توصيات ذكية بناءً على السياق والرسالة"""
        recommendations = []
        
        # Campaign optimization recommendations
        campaigns = user_context.get('campaigns', [])
        if campaigns:
            low_performing = [c for c in campaigns if float(c.get('ctr', 0)) < 2.0]
            if low_performing:
                recommendations.append("تحسين CTR للحملات منخفضة الأداء")
        
        # Content strategy recommendations
        if 'محتوى' in message or 'منشور' in message:
            if user_context.get('content_performance'):
                recommendations.append("التركيز على المحتوى التفاعلي بناءً على الأداء السابق")
            else:
                recommendations.append("بناء استراتيجية محتوى شاملة")
        
        # SEO recommendations
        if 'سيو' in message or 'تحسين' in message or 'بحث' in message:
            recommendations.append("تحليل الكلمات المفتاحية وتحسين المحتوى")
        
        # Analytics recommendations
        if 'تقرير' in message or 'إحصائيات' in message:
            recommendations.append("تركيب Google Analytics 4 وإعداد الأهداف")
        
        return ' | '.join(recommendations[:3])  # Max 3 recommendations
    
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
