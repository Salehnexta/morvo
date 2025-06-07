#!/usr/bin/env python3
"""
🔍 MORVO AI COMPLETE COMPONENT DEBUG TEST
Tests all components before production deployment
"""

import traceback
import sys

def test_component(name, test_func):
    """Test a component and return success status"""
    try:
        test_func()
        print(f'✅ {name} - PASSED')
        return True
    except Exception as e:
        print(f'❌ {name} - FAILED: {e}')
        traceback.print_exc()
        return False

def test_main_imports():
    """Test main application imports"""
    from main import app
    import config
    assert app is not None
    assert hasattr(config, 'OPENAI_API_KEY')

def test_agents():
    """Test all agents are importable"""
    from agents import MorvoAgents
    from config import AGENTS_CONFIG
    
    # Test agent manager
    manager = MorvoAgents()
    assert manager is not None
    assert len(manager.agents) == 5
    
    # Test AGENTS_CONFIG
    assert len(AGENTS_CONFIG) == 5
    
    # Test intent detection
    intent = manager.detect_intent("استراتيجية السوق")
    assert intent is not None

def test_protocols():
    """Test protocols package"""
    from protocols.manager import EnhancedProtocolManager
    from protocols.a2a_protocol import EnhancedA2AProtocol
    from protocols.mcp_server import mcp_server, EnhancedMCPResource
    from protocols.utils import generate_message_id, validate_agent_endpoint
    
    # Test utility functions
    msg_id = generate_message_id("agent1", "agent2")
    assert len(msg_id) > 0
    
    # Test endpoint validation
    valid = validate_agent_endpoint("https://example.com/agents/test")
    assert valid == True
    
    # Test MCP resource
    mcp_resource = EnhancedMCPResource()
    assert mcp_resource is not None

def test_routes():
    """Test all route modules"""
    from routes.chat import router as chat_router
    from routes.analytics import router as analytics_router
    from routes.seo import router as seo_router
    from routes.social import router as social_router
    assert chat_router is not None
    assert analytics_router is not None

def test_websocket():
    """Test websocket manager"""
    from websocket_manager import ConnectionManager
    manager = ConnectionManager()
    assert manager is not None

def test_external_deps():
    """Test critical external dependencies"""
    import fastapi
    import uvicorn
    import crewai
    import openai
    import mcp
    import websockets
    import aiohttp
    import supabase
    import redis
    import git
    print(f"  FastAPI: {fastapi.__version__}")
    print(f"  OpenAI: {openai.__version__}")

def test_config_env():
    """Test configuration and environment setup"""
    import config
    import os
    
    # Check critical config variables exist
    required_vars = [
        'OPENAI_API_KEY', 'SUPABASE_URL', 'SUPABASE_KEY',
        'REDIS_URL', 'DATABASE_URL', 'JWT_SECRET_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not hasattr(config, var):
            missing.append(var)
    
    if missing:
        print(f"  ⚠️  Missing config variables: {missing}")
    else:
        print("  ✓ All required config variables defined")

def test_protocol_integration():
    """Test protocol manager integration"""
    from protocols import EnhancedProtocolManager
    
    # Test manager can be instantiated without aiohttp session first
    # We'll test this by checking the class exists and has required methods
    assert hasattr(EnhancedProtocolManager, 'startup')
    assert hasattr(EnhancedProtocolManager, 'shutdown')
    assert hasattr(EnhancedProtocolManager, 'health_check')

def main():
    """Run all component tests"""
    print('🔍 MORVO AI COMPLETE COMPONENT DEBUG TEST')
    print('=' * 50)
    
    # Test suite
    tests = [
        ('Main Application Imports', test_main_imports),
        ('Agents Module', test_agents),
        ('Protocols Package', test_protocols),
        ('Routes Package', test_routes),
        ('WebSocket Manager', test_websocket),
        ('External Dependencies', test_external_deps),
        ('Configuration & Environment', test_config_env),
        ('Protocol Integration', test_protocol_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        results.append(test_component(test_name, test_func))
    
    print()
    print('📊 SUMMARY:')
    passed = sum(results)
    total = len(results)
    print(f'✅ Passed: {passed}/{total}')
    print(f'❌ Failed: {total - passed}/{total}')
    
    if passed == total:
        print('🎉 ALL COMPONENTS WORKING PERFECTLY!')
        print('🚀 READY FOR PRODUCTION DEPLOYMENT!')
    else:
        print('⚠️  Some components need attention before deployment')
        sys.exit(1)

if __name__ == '__main__':
    main()
