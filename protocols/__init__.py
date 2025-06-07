"""
Enhanced Protocols Package
حزمة البروتوكولات المحسنة

Modular implementation of Enhanced MCP and A2A protocols for Morvo AI
"""

from .manager import EnhancedProtocolManager
from .a2a_protocol import EnhancedA2AProtocol
from .mcp_server import mcp_server, setup_enhanced_mcp_server
from .utils import (
    generate_message_id,
    validate_agent_endpoint,
    create_jwt_token,
    verify_jwt_token,
    rate_limit,
    CircuitBreaker,
    RetryManager,
    format_resource_uri,
    parse_resource_uri,
    MessageValidator
)

__version__ = "2.0.0"
__author__ = "Morvo AI Team"

# Main exports for backward compatibility
__all__ = [
    "EnhancedProtocolManager",
    "EnhancedA2AProtocol", 
    "mcp_server",
    "setup_enhanced_mcp_server",
    "generate_message_id",
    "validate_agent_endpoint",
    "create_jwt_token",
    "verify_jwt_token",
    "rate_limit",
    "CircuitBreaker",
    "RetryManager",
    "format_resource_uri",
    "parse_resource_uri",
    "MessageValidator"
]

# Initialize logging for the package
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
