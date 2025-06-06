#!/usr/bin/env python3
"""
اختبار الوكلاء في البنية المعيارية الجديدة
Test Agents in New Modular Structure
"""

import requests
import json
from datetime import datetime

def test_chat_endpoint():
    """اختبار endpoint المحادثة مع الوكلاء"""
    print("🤖 اختبار الوكلاء في البنية الجديدة")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    test_messages = [
        {
            "message": "أريد تحليل السوق والمنافسين لشركتي",
            "expected_agent": "M1",
            "intent": "strategic_analysis"
        },
        {
            "message": "كيف أحسن أداء حملتي الإعلانية على فيسبوك؟",
            "expected_agent": "M2", 
            "intent": "social_media"
        },
        {
            "message": "أريد تحسين عائد الاستثمار لحملاتي التسويقية",
            "expected_agent": "M3",
            "intent": "campaign_optimization"
        },
        {
            "message": "أحتاج استراتيجية محتوى إبداعية لمنصاتي",
            "expected_agent": "M4",
            "intent": "content_strategy"
        },
        {
            "message": "أريد تحليل بيانات أداء موقعي وإحصائيات الزوار",
            "expected_agent": "M5",
            "intent": "data_analysis"
        }
    ]
    
    passed = 0
    total = len(test_messages)
    
    for i, test_data in enumerate(test_messages, 1):
        print(f"🧪 اختبار {i}: {test_data['intent']}")
        
        payload = {
            "content": test_data["message"],
            "user_id": f"test_user_{i}",
            "session_id": f"test_session_{i}"
        }
        
        try:
            response = requests.post(f"{base_url}/api/v2/chat/message", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ استجابة ناجحة")
                print(f"   🎯 الوكيل المكتشف: {data.get('agent_used', 'غير محدد')}")
                print(f"   🧠 النية المكتشفة: {data.get('intent_detected', 'غير محدد')}")
                print(f"   📝 بداية الاستجابة: {data.get('content', '')[:100]}...")
                passed += 1
            else:
                print(f"   ❌ فشل ({response.status_code}): {response.text}")
                
        except Exception as e:
            print(f"   ❌ خطأ: {e}")
            
        print("-" * 30)
    
    print(f"\n📊 نتائج اختبار الوكلاء:")
    print(f"✅ نجح: {passed}/{total}")
    print(f"❌ فشل: {total - passed}/{total}")
    print(f"📈 معدل النجاح: {(passed/total)*100:.1f}%")

def test_agents_status():
    """اختبار حالة الوكلاء"""
    print(f"\n🔍 اختبار حالة الوكلاء:")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8001/api/v2/chat/agents/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ حالة النظام: {data.get('status')}")
            print(f"🤖 عدد الوكلاء: {data.get('total_agents')}")
            
            agents = data.get('agents', [])
            for agent in agents:
                print(f"   - {agent['id']}: {agent['name']} ({agent['status']})")
                
        else:
            print(f"❌ فشل في جلب حالة الوكلاء: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    test_agents_status()
    print("\n" + "="*50)
    test_chat_endpoint()
    
    print(f"\n📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 اختبار الوكلاء في البنية الجديدة مكتمل!")
