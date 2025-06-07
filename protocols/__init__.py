"""
Enhanced Protocols Package
حزمة البروتوكولات المحسنة

Modular implementation of Enhanced MCP and A2A protocols for Morvo AI
"""

# Import core components that are always available
from .manager import EnhancedProtocolManager
from .a2a_protocol import EnhancedA2AProtocol

# Import utilities
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

# Optional MCP imports - handle gracefully if MCP is not available
try:
    from .mcp_server import mcp_server, setup_enhanced_mcp_server
    MCP_AVAILABLE = True
except ImportError:
    mcp_server = None
    setup_enhanced_mcp_server = None
    MCP_AVAILABLE = False

__version__ = "2.0.0"
__author__ = "Morvo AI Team"

__all__ = [
    'EnhancedProtocolManager',
    'EnhancedA2AProtocol',
    'generate_message_id',
    'validate_agent_endpoint', 
    'create_jwt_token',
    'verify_jwt_token',
    'rate_limit',
    'CircuitBreaker',
    'RetryManager',
    'format_resource_uri',
    'parse_resource_uri',
    'MessageValidator',
    'MCP_AVAILABLE'
]

# Add MCP components to exports if available
if MCP_AVAILABLE:
    __all__.extend(['mcp_server', 'setup_enhanced_mcp_server'])

# Initialize logging for the package
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
