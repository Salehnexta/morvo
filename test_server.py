#!/usr/bin/env python3
"""
Test script for Morvo AI Production Server
اختبار خادم Morvo AI الإنتاجي
"""

import requests
import json

SERVER_URL = "https://morvo-production.up.railway.app"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a server endpoint"""
    url = f"{SERVER_URL}{endpoint}"
    print(f"🔍 Testing {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Success: {response.json()}")
        else:
            print(f"   ❌ Error: {response.text}")
        print()
        
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        print()

def main():
    print("🚀 Testing Morvo AI Production Server")
    print(f"🌐 Server: {SERVER_URL}")
    print("=" * 50)
    
    # Test basic endpoints
    test_endpoint("/health")
    test_endpoint("/health/detailed")
    
    # Test protocol endpoints
    test_endpoint("/protocols/status")
    test_endpoint("/mcp/resources")
    test_endpoint("/a2a/network")
    
    # Test chat endpoint
    chat_data = {
        "message": "مرحبا، اختبار MCP",
        "user_id": "test_user_123"
    }
    test_endpoint("/chat", "POST", chat_data)
    
    print("🏁 Testing complete!")

if __name__ == "__main__":
    main()
