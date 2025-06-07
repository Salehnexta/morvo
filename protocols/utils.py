"""
Protocol Utilities
أدوات مساعدة للبروتوكولات

Common utilities for MCP and A2A protocols
"""

import logging
import hashlib
import jwt
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)


def generate_message_id(from_agent: str, to_agent: str, timestamp: Optional[str] = None) -> str:
    """توليد معرف فريد للرسالة"""
    if not timestamp:
        timestamp = datetime.now().isoformat()
    
    return hashlib.sha256(
        f"{from_agent}{to_agent}{timestamp}".encode()
    ).hexdigest()[:16]


def validate_agent_endpoint(endpoint: str) -> bool:
    """التحقق من صحة نقطة نهاية الوكيل"""
    try:
        # Basic URL validation
        if not endpoint.startswith(('http://', 'https://')):
            return False
        
        # Check for required path structure
        if '/agents/' not in endpoint:
            return False
            
        return True
    except Exception:
        return False


def create_jwt_token(agent_id: str, secret_key: str, expires_hours: int = 24) -> str:
    """إنشاء رمز JWT للمصادقة"""
    payload = {
        'agent_id': agent_id,
        'exp': datetime.utcnow() + timedelta(hours=expires_hours),
        'iat': datetime.utcnow(),
        'iss': 'morvo-a2a-protocol'
    }
    
    return jwt.encode(payload, secret_key, algorithm='HS256')


def verify_jwt_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """التحقق من رمز JWT"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid JWT token")
        return None


def rate_limit(calls_per_minute: int = 60):
    """محدد معدل الاستدعاءات"""
    call_times = []
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = datetime.now()
            
            # Remove calls older than 1 minute
            call_times[:] = [t for t in call_times if (now - t).seconds < 60]
            
            if len(call_times) >= calls_per_minute:
                raise Exception(f"Rate limit exceeded: {calls_per_minute} calls per minute")
            
            call_times.append(now)
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


class CircuitBreaker:
    """قاطع الدائرة للحماية من الأخطاء المتتالية"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == 'OPEN':
                if self._should_attempt_reset():
                    self.state = 'HALF_OPEN'
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise e
        
        return wrapper
    
    def _should_attempt_reset(self) -> bool:
        """التحقق من إمكانية إعادة المحاولة"""
        if self.last_failure_time is None:
            return True
        
        return (datetime.now() - self.last_failure_time).seconds >= self.recovery_timeout
    
    def _on_success(self):
        """عند نجاح العملية"""
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def _on_failure(self):
        """عند فشل العملية"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'


class RetryManager:
    """مدير إعادة المحاولة مع تأخير متزايد"""
    
    @staticmethod
    async def retry_with_backoff(
        func,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0
    ):
        """إعادة المحاولة مع تأخير متزايد"""
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return await func()
            except Exception as e:
                last_exception = e
                
                if attempt == max_retries:
                    break
                
                delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}")
                await asyncio.sleep(delay)
        
        raise last_exception


def format_resource_uri(resource_type: str, resource_path: str, operation: Optional[str] = None) -> str:
    """تنسيق URI للموارد"""
    uri = f"{resource_type}://{resource_path}"
    if operation:
        uri += f"/{operation}"
    return uri


def parse_resource_uri(uri: str) -> Dict[str, str]:
    """تحليل URI للموارد"""
    try:
        if '://' not in uri:
            raise ValueError("Invalid URI format")
        
        protocol, path = uri.split('://', 1)
        path_parts = path.split('/')
        
        return {
            'protocol': protocol,
            'resource': path_parts[0] if path_parts else '',
            'operation': path_parts[1] if len(path_parts) > 1 else '',
            'params': path_parts[2:] if len(path_parts) > 2 else []
        }
    except Exception as e:
        logger.error(f"Failed to parse URI {uri}: {str(e)}")
        return {}


def sanitize_agent_id(agent_id: str) -> str:
    """تنظيف معرف الوكيل"""
    # Remove special characters and ensure valid format
    sanitized = ''.join(c for c in agent_id if c.isalnum() or c in '-_')
    return sanitized[:50]  # Limit length


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """تنسيق الوقت بصيغة ISO"""
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()


def calculate_message_hash(message: Dict[str, Any]) -> str:
    """حساب hash للرسالة"""
    import json
    message_str = json.dumps(message, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(message_str.encode()).hexdigest()


class MessageValidator:
    """مُحقق صحة الرسائل"""
    
    @staticmethod
    def validate_a2a_message(message: Dict[str, Any]) -> bool:
        """التحقق من صحة رسالة A2A"""
        required_fields = ['from', 'to', 'message', 'timestamp']
        
        for field in required_fields:
            if field not in message:
                logger.error(f"Missing required field: {field}")
                return False
        
        # Validate agent IDs
        if not isinstance(message['from'], str) or not message['from'].strip():
            logger.error("Invalid 'from' agent ID")
            return False
        
        if not isinstance(message['to'], str) or not message['to'].strip():
            logger.error("Invalid 'to' agent ID")
            return False
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            logger.error("Invalid timestamp format")
            return False
        
        return True
    
    @staticmethod
    def validate_mcp_resource_uri(uri: str) -> bool:
        """التحقق من صحة URI للمورد MCP"""
        supported_protocols = ['supabase', 'git', 'file', 'redis']
        
        try:
            parsed = parse_resource_uri(uri)
            return parsed.get('protocol') in supported_protocols
        except Exception:
            return False
