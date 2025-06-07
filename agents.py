"""
Enhanced Morvo AI Agents with MCP & A2A Protocol Integration
النظام المحسن لوكلاء Morvo AI مع دمج بروتوكولات MCP و A2A
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

class MCPProtocol:
    """بروتوكول MCP لإدارة الموارد والبيانات"""
    
    def __init__(self):
        self.resources: Dict[str, Any] = {}
        self.supabase_client: Optional[Client] = None
        self._initialize_supabase()
    
    def _initialize_supabase(self):
        """تهيئة عميل Supabase للـ MCP"""
        if not SUPABASE_AVAILABLE:
            return
            
        try:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
            
            if supabase_url and supabase_key:
                self.supabase_client = create_client(supabase_url, supabase_key)
                logger.info("✅ Supabase MCP client initialized")
            else:
                logger.warning("⚠️ Supabase credentials missing for MCP")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Supabase MCP client: {e}")
    
    async def register_resource(self, uri: str, resource_type: str, data: Any = None):
        """تسجيل مورد MCP"""
        try:
            self.resources[uri] = {
                "type": resource_type,
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "access_count": 0
            }
            logger.info(f"📝 MCP resource registered: {uri}")
        except Exception as e:
            logger.error(f"❌ Failed to register MCP resource {uri}: {e}")
    
    async def get_resource(self, uri: str) -> Optional[Any]:
        """الحصول على مورد MCP"""
        try:
            if uri not in self.resources:
                # Try to load from Supabase if available
                await self._load_supabase_resource(uri)
            
            if uri in self.resources:
                self.resources[uri]["access_count"] += 1
                return self.resources[uri]["data"]
            return None
        except Exception as e:
            logger.error(f"❌ Failed to get MCP resource {uri}: {e}")
            return None
    
    async def _load_supabase_resource(self, uri: str):
        """تحميل مورد من Supabase"""
        if not self.supabase_client:
            return
            
        try:
            # Parse URI to determine table and query
            if uri.startswith("data://supabase/"):
                table_name = uri.replace("data://supabase/", "")
                
                # Load data from Supabase table
                if table_name == "profiles":
                    response = self.supabase_client.table("profiles").select("*").limit(100).execute()
                elif table_name == "campaigns":
                    response = self.supabase_client.table("marketing_campaigns").select("*").limit(50).execute()
                elif table_name == "analytics":
                    response = self.supabase_client.table("analytics_data").select("*").limit(100).execute()
                elif table_name == "conversations":
                    response = self.supabase_client.table("morvo_conversations").select("*").limit(200).execute()
                elif table_name == "unified_customer_data":
                    response = self.supabase_client.table("unified_customer_data").select("*").limit(100).execute()
                else:
                    return
                
                if response.data:
                    await self.register_resource(uri, "supabase_table", response.data)
                    logger.info(f"📊 Loaded {len(response.data)} records from {table_name}")
                    
        except Exception as e:
            logger.error(f"❌ Failed to load Supabase resource {uri}: {e}")
    
    async def call_tool(self, tool_name: str, parameters: Dict) -> Any:
        """استدعاء أداة MCP"""
        try:
            # Implement tool calling logic
            if tool_name == "supabase_query":
                return await self._execute_supabase_query(parameters)
            elif tool_name == "data_analysis":
                return await self._analyze_data(parameters)
            else:
                logger.warning(f"⚠️ Unknown MCP tool: {tool_name}")
                return None
        except Exception as e:
            logger.error(f"❌ Failed to call MCP tool {tool_name}: {e}")
            return None
    
    async def _execute_supabase_query(self, parameters: Dict) -> Any:
        """تنفيذ استعلام Supabase عبر MCP"""
        if not self.supabase_client:
            return {"error": "Supabase client not available"}
            
        try:
            table = parameters.get("table")
            filters = parameters.get("filters", {})
            limit = parameters.get("limit", 100)
            
            query = self.supabase_client.table(table).select("*")
            
            # Apply filters
            for column, value in filters.items():
                query = query.eq(column, value)
            
            response = query.limit(limit).execute()
            return {"data": response.data, "count": len(response.data)}
            
        except Exception as e:
            logger.error(f"❌ Supabase query error: {e}")
            return {"error": str(e)}

    async def get_supabase_kpi_context(self, user_id: str) -> Dict[str, Any]:
        """الحصول على سياق المؤشرات الرئيسية من Supabase"""
        if not self.supabase_client:
            return {}
            
        try:
            context = {}
            
            # Get user profile
            profile_response = self.supabase_client.table("profiles").select("*").eq("id", user_id).execute()
            if profile_response.data:
                context["user_profile"] = profile_response.data[0]
            
            # Get campaigns count
            campaigns_response = self.supabase_client.table("marketing_campaigns").select("*").eq("user_id", user_id).execute()
            context["total_campaigns"] = len(campaigns_response.data) if campaigns_response.data else 0
            
            # Get recent analytics
            analytics_response = self.supabase_client.table("analytics_data").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(10).execute()
            context["recent_analytics"] = analytics_response.data if analytics_response.data else []
            
            # Get conversation history
            conversations_response = self.supabase_client.table("morvo_conversations").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(5).execute()
            context["recent_conversations"] = conversations_response.data if conversations_response.data else []
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get Supabase KPI context: {e}")
            return {}

class A2AProtocol:
    """Agent-to-Agent communication protocol"""
    
    def __init__(self):
        self.agent_endpoints = {}
        self.message_queue = asyncio.Queue()
    
    async def register_agent(self, agent_id: str, endpoints: List[str]):
        """Register agent endpoints for A2A communication"""
        self.agent_endpoints[agent_id] = endpoints
    
    async def send_message(self, from_agent: str, to_agent: str, endpoint: str, payload: Dict):
        """Send message between agents"""
        message = {
            "from": from_agent,
            "to": to_agent,
            "endpoint": endpoint,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        }
        await self.message_queue.put(message)
        return {"status": "sent", "message_id": hash(str(message))}
    
    async def receive_message(self, agent_id: str) -> Optional[Dict]:
        """Receive message for agent"""
        try:
            message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
            if message["to"] == agent_id:
                return message
            else:
                # Put back if not for this agent
                await self.message_queue.put(message)
                return None
        except asyncio.TimeoutError:
            return None

class EnhancedMorvoAgents:
    """مدير الوكلاء المتخصصين مع MCP و A2A"""
    
    def __init__(self):
        self.mcp = MCPProtocol()
        self.a2a = A2AProtocol()
        self.agents = self._create_agents()
        
        # Initialize MCP resources and A2A endpoints
        asyncio.create_task(self._initialize_protocols())
    
    def _create_agents(self) -> Dict[str, Agent]:
        """إنشاء جميع الوكلاء المتخصصين مع MCP و A2A"""
        agents = {}
        
        for agent_config in AGENTS_CONFIG:
            # Enhanced agent with MCP and A2A capabilities
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=f"{agent_config['backstory']}\n\nقدرات MCP: {', '.join(agent_config['mcp_resources'])}\nنقاط A2A: {', '.join(agent_config['a2a_endpoints'])}",
                verbose=True,
                allow_delegation=True,
                max_iter=3,
                memory=True
            )
            agents[agent_config["id"]] = agent
            
        return agents
    
    async def _initialize_protocols(self):
        """Initialize MCP resources and A2A endpoints"""
        try:
            # Register MCP resources for each agent
            for agent_config in AGENTS_CONFIG:
                agent_id = agent_config["id"]
                
                # Register A2A endpoints
                await self.a2a.register_agent(agent_id, agent_config["a2a_endpoints"])
                
                # Register MCP resources
                for resource_uri in agent_config["mcp_resources"]:
                    if resource_uri.startswith("data://supabase/"):
                        # Load Supabase data as MCP resource
                        data = await self.mcp.get_resource(resource_uri)
                        if data:
                            await self.mcp.register_resource(resource_uri, "database", data)
                    elif resource_uri.startswith("schema://"):
                        # Load schema information
                        schema_data = await self.mcp.get_resource(resource_uri)
                        if schema_data:
                            await self.mcp.register_resource(resource_uri, "schema", schema_data)
            
            logger.info("MCP and A2A protocols initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing protocols: {e}")
    
    async def process_message(self, user_id: str, message: str, filters: Dict = None) -> Dict[str, Any]:
        """معالجة الرسالة مع MCP و A2A المحسنة"""
        logger.info(f"🔄 Processing message with enhanced MCP & A2A for user: {user_id}")
        
        try:
            # Import MCP connector
            from mcp_connector import get_mcp_connector
            mcp_connector = get_mcp_connector()
            
            # Get user context via MCP
            user_context = await mcp_connector.get_user_data(user_id)
            
            # Detect intent
            intent = self.detect_intent(message)
            
            # Select primary agent
            primary_agent = self.get_primary_agent(intent)
            
            # Get collaborating agents for A2A
            collaborating_agents = self.get_collaborating_agents(intent, primary_agent)
            
            # Create enhanced prompt with MCP context
            enhanced_message = f"""
{message}

السياق المحدث من MCP:
- إجمالي الحملات: {user_context.get('total_campaigns', 0)}
- MCP مُفعل: {user_context.get('mcp_enabled', False)}
- البيانات متوفرة: {bool(user_context.get('profile'))}
"""
            
            # Process with primary agent
            response = primary_agent.crew.kickoff({
                'message': enhanced_message,
                'user_context': user_context,
                'intent': intent,
                'user_id': user_id
            })
            
            # A2A collaboration
            if collaborating_agents:
                collaboration_results = []
                for agent_name in collaborating_agents:
                    if agent_name in self.agents:
                        collab_agent = self.agents[agent_name]
                        collab_response = collab_agent.crew.kickoff({
                            'original_response': response,
                            'context': user_context,
                            'collaboration_mode': True
                        })
                        collaboration_results.append({
                            'agent': agent_name,
                            'contribution': str(collab_response)[:200]  # Summary
                        })
                
                # Merge collaborative insights
                if collaboration_results:
                    enhanced_response = f"{response}\n\n[تحسينات من A2A: {len(collaboration_results)} وكلاء متعاونين]"
                else:
                    enhanced_response = response
            else:
                enhanced_response = response
            
            # Save conversation via MCP
            await mcp_connector.save_conversation(
                user_id=user_id,
                content=message,
                response=str(enhanced_response),
                context={
                    "intent": intent,
                    "primary_agent": primary_agent.role,
                    "collaborating_agents": collaborating_agents,
                    "mcp_context": user_context,
                    "protocols_used": ["MCP", "A2A"]
                }
            )
            
            return {
                "response": str(enhanced_response),
                "intent": intent,
                "primary_agent": primary_agent.role,
                "collaborating_agents": collaborating_agents,
                "user_context": user_context,
                "mcp_enabled": user_context.get('mcp_enabled', False),
                "a2a_collaboration": len(collaboration_results) if 'collaboration_results' in locals() else 0
            }
            
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الرسالة: {e}")
            return {
                "response": f"عذراً، حدث خطأ في المعالجة. {str(e)[:100]}",
                "error": str(e),
                "mcp_enabled": False
            }
    
    async def _gather_mcp_context(self, agent_id: str, intent: str) -> Dict:
        """جمع السياق عبر MCP"""
        context = {}
        agent_config = next((a for a in AGENTS_CONFIG if a["id"] == agent_id), None)
        
        if agent_config:
            for resource_uri in agent_config["mcp_resources"]:
                resource_data = await self.mcp.get_resource(resource_uri)
                if resource_data:
                    context[resource_uri] = resource_data
        
        return context
    
    async def _enable_a2a_collaboration(self, primary_agent: str, collaborators: List[str], 
                                      content: str, context: Dict) -> Dict:
        """تمكين التعاون A2A بين الوكلاء"""
        collaboration_results = {}
        
        for collaborator in collaborators:
            # Send collaboration request
            payload = {
                "request_type": "collaborate",
                "primary_agent": primary_agent,
                "user_content": content,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
            result = await self.a2a.send_message(
                primary_agent, collaborator, "collaboration", payload
            )
            
            collaboration_results[collaborator] = {
                "message_sent": result["status"] == "sent",
                "capabilities": next((a["capabilities"] for a in AGENTS_CONFIG if a["id"] == collaborator), []),
                "specialization": next((a["role"] for a in AGENTS_CONFIG if a["id"] == collaborator), "Unknown")
            }
        
        return collaboration_results
    
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
