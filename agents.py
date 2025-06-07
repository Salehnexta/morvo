"""
Agents Management for Morvo AI
إدارة الوكلاء لـ Morvo AI
"""

import logging
from crewai import Agent, Task, Crew, Process
from openai import OpenAI
from config import AGENTS_CONFIG, OPENAI_API_KEY
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class MorvoAgents:
    """مدير الوكلاء المتخصصين"""
    
    def __init__(self):
        # CrewAI now handles OpenAI integration internally
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.agents = self._create_agents()
        
    def _create_agents(self) -> Dict[str, Agent]:
        """إنشاء جميع الوكلاء المتخصصين"""
        agents = {}
        
        for agent_config in AGENTS_CONFIG:
            # Latest CrewAI automatically handles LLM configuration
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                verbose=True,
                allow_delegation=True,
                max_iter=3,
                memory=True
            )
            agents[agent_config["id"]] = agent
            
        return agents
    
    def detect_intent(self, message: str) -> str:
        """كشف نية المستخدم من الرسالة"""
        message_lower = message.lower()
        
        # Strategic analysis intent
        if any(keyword in message_lower for keyword in ["استراتيجية", "تحليل سوق", "منافسين", "تموضع", "خطة"]):
            return "strategic_analysis"
            
        # Social media intent  
        elif any(keyword in message_lower for keyword in ["سوشيال", "تواصل", "فيسبوك", "انستغرام", "تويتر", "لينكد"]):
            return "social_media"
            
        # Campaign optimization intent
        elif any(keyword in message_lower for keyword in ["حملة", "إعلان", "تحسين", "roi", "ميزانية", "أداء"]):
            return "campaign_optimization"
            
        # Content strategy intent
        elif any(keyword in message_lower for keyword in ["محتوى", "كتابة", "منشور", "مقال", "فيديو", "تقويم"]):
            return "content_strategy"
            
        # Data analysis intent
        elif any(keyword in message_lower for keyword in ["بيانات", "تحليل", "إحصائيات", "أرقام", "تقرير", "رؤى"]):
            return "data_analysis"
            
        else:
            return "general_inquiry"
    
    def select_primary_agent(self, intent: str) -> str:
        """اختيار الوكيل الأساسي حسب النية"""
        intent_to_agent = {
            "strategic_analysis": "M1",
            "social_media": "M2", 
            "campaign_optimization": "M3",
            "content_strategy": "M4",
            "data_analysis": "M5",
            "general_inquiry": "M1"  # Default to strategic analyst
        }
        return intent_to_agent.get(intent, "M1")
    
    def get_collaborating_agents(self, primary_agent: str) -> List[str]:
        """الحصول على الوكلاء المتعاونين"""
        all_agents = ["M1", "M2", "M3", "M4", "M5"]
        collaborators = [agent for agent in all_agents if agent != primary_agent]
        return collaborators[:2]  # اختيار أول 2 وكلاء متعاونين
    
    async def process_message(self, content: str, user_id: str, session_id: str) -> Dict:
        """معالجة رسالة المستخدم"""
        try:
            # كشف النية
            intent = self.detect_intent(content)
            primary_agent_id = self.select_primary_agent(intent)
            collaborating_agents = self.get_collaborating_agents(primary_agent_id)
            
            # إنشاء المهمة
            task = Task(
                description=f"""
                تحليل وإجابة الاستفسار التالي من المستخدم:
                "{content}"
                
                المطلوب:
                1. فهم السؤال أو الطلب بدقة
                2. تقديم إجابة شاملة ومفيدة باللغة العربية
                3. تقديم توصيات عملية قابلة للتنفيذ
                4. استخدام الخبرة المتخصصة في المجال
                
                معرف المستخدم: {user_id}
                معرف الجلسة: {session_id}
                النية المكتشفة: {intent}
                """,
                agent=self.agents[primary_agent_id],
                expected_output="إجابة شاملة باللغة العربية مع توصيات عملية"
            )
            
            # إنشاء الفريق
            crew_agents = [self.agents[primary_agent_id]]
            for collab_id in collaborating_agents:
                crew_agents.append(self.agents[collab_id])
            
            crew = Crew(
                agents=crew_agents,
                tasks=[task],
                verbose=True,
                process=Process.sequential,
                memory=True
            )
            
            # تنفيذ المهمة
            result = crew.kickoff()
            
            return {
                "content": str(result),
                "agent_used": primary_agent_id,
                "collaborating_agents": collaborating_agents,
                "intent_detected": intent,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"خطأ في معالجة الرسالة: {e}")
            return {
                "content": "أعتذر، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى.",
                "agent_used": "error",
                "intent_detected": "error",
                "session_id": session_id
            }
    
    def get_agents_status(self) -> List[Dict]:
        """الحصول على حالة جميع الوكلاء"""
        status = []
        for agent_config in AGENTS_CONFIG:
            status.append({
                "id": agent_config["id"],
                "name": agent_config["name"], 
                "status": "active",
                "specialization": agent_config["role"]
            })
        return status
