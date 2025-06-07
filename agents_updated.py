"""
Unified Morvo AI Companion
رفيق مورفو الموحد للتسويق الذكي
"""

import asyncio
import logging
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedMorvoCompanion:
    """
    Unified Marketing Companion for Morvo AI
    رفيق تسويق موحد لـ مورفو الذكية
    """
    
    def __init__(self, supabase_client=None):
        """Initialize the unified companion"""
        self.supabase = supabase_client
        self.system_prompt = None
        self.version = "2.0.0"
        self.initialized = False
        self._initialize()
    
    def _initialize(self):
        """Initialize the companion asynchronously"""
        try:
            # Load system prompt
            asyncio.create_task(self._load_system_prompt())
            self.initialized = True
            logger.info("✅ Unified Morvo Companion initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing Morvo Companion: {e}")
    
    async def _load_system_prompt(self):
        """Load the system prompt from database or use default"""
        try:
            if self.supabase:
                result = self.supabase.table('prompts') \
                    .select('content') \
                    .eq('name', 'morvo_unified_companion') \
                    .eq('is_active', True) \
                    .order('version', desc=True) \
                    .limit(1) \
                    .execute()
                
                if result.data:
                    self.system_prompt = result.data[0]['content']
                    logger.info("✅ Loaded system prompt from database")
                    return
            
            # Fallback to default prompt
            self.system_prompt = """
            أنت «مورفو» – رفيق تسويق ذكي واحد.
            • تحدُّث بالعربية الفصحى بلمسة خليجية ودودة.
            • وظيفتك تبسيط التسويق: تحليل SEO، أفكار محتوى، حملات، تتبّع ROI.
            • لا تذكر أي لوحة تحكّم أو جداول معقّدة؛ كل شيء يتمّ داخل المحادثة.
            • جمَل قصيرة، أفعال مباشرة، إيموجي واحد كحدّ أقصى.
            • لا تتجاوز 300 كلمة في أي ردّ.
            • ركّز على ربط كل شيء بأهداف العمل وقياس الأداء.
            """
            logger.info("✅ Using default system prompt")
            
        except Exception as e:
            logger.error(f"❌ Error loading system prompt: {e}")
            self.system_prompt = "مرحباً! أنا مورفو، مساعدك الذكي في التسويق. كيف يمكنني مساعدتك اليوم؟"
    
    async def process_message(self, user_id: str, message: str, context: Dict = None) -> Dict[str, Any]:
        """
        Process a user message with the unified companion
        معالجة رسالة المستخدم باستخدام رفيق مورفو الموحد
        """
        if not self.initialized:
            return {"status": "error", "message": "Companion not initialized"}
        
        try:
            # Log the conversation
            await self._log_conversation(user_id, message, context)
            
            # Prepare the prompt with context
            prompt = self._prepare_prompt(message, context)
            
            # Generate response (in a real implementation, this would call an LLM)
            response = await self._generate_response(prompt)
            
            # Save the assistant's response
            await self._log_conversation(user_id, response, context, is_assistant=True)
            
            return {
                "status": "success",
                "response": response,
                "context": context or {}
            }
            
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _prepare_prompt(self, message: str, context: Dict = None) -> str:
        """Prepare the prompt with context"""
        context_str = json.dumps(context, ensure_ascii=False) if context else "لا يوجد سياق إضافي"
        
        prompt = f"""
        {self.system_prompt}
        
        السياق الحالي:
        {context_str}
        
        رسالة المستخدم:
        {message}
        
        الرد:
        """
        return prompt
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate a response using the LLM"""
        # In a real implementation, this would call an LLM API
        # For now, we'll return a simple response
        return "مرحباً! شكراً لتواصلك مع مورفو. كيف يمكنني مساعدتك في استراتيجية التسويق الخاصة بك اليوم؟"
    
    async def _log_conversation(self, user_id: str, message: str, context: Dict = None, is_assistant: bool = False):
        """Log the conversation to the database"""
        if not self.supabase:
            return
            
        try:
            conversation_data = {
                "user_id": user_id,
                "message": message,
                "is_assistant": is_assistant,
                "context_data": context or {},
                "created_at": datetime.utcnow().isoformat()
            }
            
            self.supabase.table('conversations').insert(conversation_data).execute()
            
        except Exception as e:
            logger.error(f"❌ Error logging conversation: {e}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get the status of the companion"""
        return {
            "status": "active",
            "version": self.version,
            "initialized": self.initialized,
            "system_prompt_loaded": bool(self.system_prompt)
        }

# For backward compatibility
class EnhancedMorvoAgents:
    """Legacy wrapper for backward compatibility"""
    def __init__(self):
        self.morvo_companion = UnifiedMorvoCompanion()
        logger.info("🤖 Initialized EnhancedMorvoAgents with UnifiedMorvoCompanion")
    
    async def process_message(self, user_id: str, message: str, filters: Dict = None):
        return await self.morvo_companion.process_message(user_id, message, filters)
    
    def get_agents_status(self):
        return {
            "status": "active",
            "version": self.morvo_companion.version,
            "type": "unified_companion"
        }

# Legacy class for backward compatibility
class MorvoAgents(EnhancedMorvoAgents):
    """Legacy wrapper for backward compatibility"""
    def __init__(self):
        super().__init__()
        logger.info("🔄 Legacy MorvoAgents initialized - Using UnifiedMorvoCompanion")

# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize with a mock supabase client for testing
        class MockSupabase:
            def table(self, name):
                return self
            def insert(self, data):
                return self
            def execute(self):
                return type('obj', (object,), {'data': []})
            def select(self, *args):
                return self
            def eq(self, *args):
                return self
            def order(self, *args, **kwargs):
                return self
            def limit(self, *args):
                return self
        
        supabase = MockSupabase()
        companion = UnifiedMorvoCompanion(supabase)
        
        # Test the companion
        response = await companion.process_message(
            user_id="test_user_123",
            message="مرحباً، كيف يمكنك مساعدتي في تحسين ظهور موقعي في محركات البحث؟",
            context={"industry": "ecommerce", "language": "ar"}
        )
        
        print("\nResponse:", json.dumps(response, ensure_ascii=False, indent=2))
        
        # Get status
        status = await companion.get_status()
        print("\nStatus:", json.dumps(status, ensure_ascii=False, indent=2))
    
    asyncio.run(main())
