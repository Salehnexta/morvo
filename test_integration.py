#!/usr/bin/env python3
"""
اختبار تكامل مزودي البيانات التسويقية
Morvo AI Marketing Providers Integration Test
"""

import asyncio
import json
import requests
from datetime import datetime

def test_basic_health():
    """اختبار الصحة الأساسية"""
    print("🏥 اختبار الصحة الأساسية...")
    
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ الصحة: {data['status']}")
            print(f"📊 الوكلاء: {len(data['agents'])} وكيل")
            return True
        else:
            print(f"❌ فشل اختبار الصحة: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False

def test_providers_status():
    """اختبار حالة مزودي البيانات"""
    print("\n📊 اختبار حالة مزودي البيانات...")
    
    try:
        response = requests.get("http://localhost:8000/api/v2/analytics/providers/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ حالة المزودين: {data['status']}")
            if 'expected_providers' in data:
                print("📋 المزودون المتوقعون:")
                for provider, plan in data['expected_providers'].items():
                    print(f"   - {provider}: {plan}")
            return True
        else:
            print(f"❌ فشل اختبار المزودين: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في اختبار المزودين: {e}")
        return False

def test_comprehensive_analysis():
    """اختبار التحليل الشامل"""
    print("\n🔍 اختبار التحليل الشامل...")
    
    payload = {
        "brand": "شركة تقنية سعودية",
        "keywords": ["تسويق رقمي", "سيو", "وسائل التواصل الاجتماعي"],
        "analysis_type": "comprehensive"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v2/analytics/comprehensive",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ التحليل الشامل: {data['status']}")
            print(f"📝 الرسالة: {data['message']}")
            if 'expected_features' in data:
                print("🎯 الميزات المتوقعة:")
                for feature in data['expected_features']:
                    print(f"   - {feature}")
            return True
        else:
            print(f"❌ فشل التحليل الشامل: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في التحليل الشامل: {e}")
        return False

def test_seo_keywords():
    """اختبار تحليل الكلمات المفتاحية"""
    print("\n🔍 اختبار تحليل SEO...")
    
    payload = ["تسويق رقمي", "استراتيجية تسويق", "وسائل التواصل"]
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v2/seo/keywords",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ تحليل SEO: {data['status']}")
            print(f"📝 الرسالة: {data['message']}")
            if 'features_coming' in data:
                print("🎯 الميزات القادمة:")
                for feature in data['features_coming']:
                    print(f"   - {feature}")
            return True
        else:
            print(f"❌ فشل تحليل SEO: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في تحليل SEO: {e}")
        return False

def test_social_schedule():
    """اختبار جدولة المنشورات الاجتماعية"""
    print("\n📱 اختبار جدولة المنشورات...")
    
    payload = {
        "content": "منشور تجريبي من مورفو AI 🚀",
        "platforms": ["facebook", "twitter", "instagram"],
        "schedule_time": "2024-12-07T10:00:00"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v2/social/schedule-post",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ جدولة المنشورات: {data['status']}")
            print(f"📝 الرسالة: {data['message']}")
            if 'features_coming' in data:
                print("🎯 الميزات القادمة:")
                for feature in data['features_coming']:
                    print(f"   - {feature}")
            return True
        else:
            print(f"❌ فشل جدولة المنشورات: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في جدولة المنشورات: {e}")
        return False

def test_social_inbox():
    """اختبار صندوق الوارد الاجتماعي"""
    print("\n📬 اختبار صندوق الوارد...")
    
    try:
        response = requests.get("http://localhost:8000/api/v2/social/inbox")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ صندوق الوارد: {data['status']}")
            print(f"📝 الرسالة: {data['message']}")
            if 'features_coming' in data:
                print("🎯 الميزات القادمة:")
                for feature in data['features_coming']:
                    print(f"   - {feature}")
            return True
        else:
            print(f"❌ فشل صندوق الوارد: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في صندوق الوارد: {e}")
        return False

def test_chat_with_agents():
    """اختبار المحادثة مع الوكلاء"""
    print("\n🤖 اختبار المحادثة مع الوكلاء...")
    
    payload = {
        "content": "أحتاج تحليل شامل لاستراتيجية التسويق الرقمي",
        "user_id": "test_integration",
        "session_id": "integration_test_session"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v2/chat/message",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ المحادثة: نجحت")
            print(f"🧠 الهدف المكتشف: {data.get('intent_detected', 'غير محدد')}")
            print(f"💬 الرد: {data['content'][:100]}...")
            return True
        else:
            print(f"❌ فشل المحادثة: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في المحادثة: {e}")
        return False

def main():
    """تشغيل جميع الاختبارات"""
    print("🚀 بدء اختبار التكامل الشامل لـ Morvo AI")
    print("=" * 50)
    
    tests = [
        test_basic_health,
        test_providers_status,
        test_comprehensive_analysis,
        test_seo_keywords,
        test_social_schedule,
        test_social_inbox,
        test_chat_with_agents
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 نتائج الاختبار:")
    print(f"✅ نجح: {passed}/{total}")
    print(f"❌ فشل: {total - passed}/{total}")
    print(f"📈 معدل النجاح: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 جميع الاختبارات نجحت! النظام جاهز للأسبوع القادم.")
    else:
        print(f"\n⚠️  {total - passed} اختبارات فشلت. يرجى المراجعة.")
    
    print(f"\n📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔜 مزودو البيانات سيتم تفعيلهم الأسبوع القادم!")

if __name__ == "__main__":
    main()
