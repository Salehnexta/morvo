"""
Pydantic Models for Morvo AI
نماذج البيانات لـ Morvo AI
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# Chat models
class ChatMessage(BaseModel):
    content: str
    user_id: str
    session_id: Optional[str] = None
    timestamp: Optional[datetime] = None

class ChatResponse(BaseModel):
    content: str
    agent_used: str
    intent_detected: str
    timestamp: datetime
    session_id: str

# Marketing Analytics models
class AnalyticsRequest(BaseModel):
    brand: str
    keywords: List[str]
    analysis_type: str = "comprehensive"

class AnalysisRequest(BaseModel):
    brand: str
    keywords: List[str]
    timeframe: Optional[str] = "30d"
    competitors: Optional[List[str]] = []

# Social Media models
class SocialPostRequest(BaseModel):
    content: str
    platforms: List[str]
    schedule_time: Optional[str] = None
    media_urls: Optional[List[str]] = []

# Webhook models
class AwarioWebhookData(BaseModel):
    mention_id: str
    content: str
    source: str
    sentiment: str
    author: str
    url: str
    timestamp: datetime

# Response models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    agents: List[Dict[str, str]]

class ProvidersStatusResponse(BaseModel):
    status: str
    message: str
    expected_providers: Dict[str, str]
    activation_date: str
    total_cost: Optional[str] = None
