#!/usr/bin/env python3
"""
اختبار البنية المعيارية الجديدة لـ Morvo AI
Test New Modular Structure for Morvo AI
"""

import requests
import json
from datetime import datetime

def test_new_structure():
    """اختبار البنية الجديدة"""
    print("🧩 اختبار البنية المعيارية الجديدة لـ Morvo AI")
    print("=" * 50)
    
    base_url = "http://localhost:8001"  # منفذ مختلف للاختبار
    
    tests = [
        ("GET", "/", "الصفحة الرئيسية"),
        ("GET", "/health", "فحص الصحة"),
        ("GET", "/api/v2/analytics/providers/status", "حالة مزودي البيانات"),
        ("POST", "/api/v2/analytics/comprehensive", "التحليل الشامل"),
        ("POST", "/api/v2/seo/keywords", "تحليل الكلمات المفتاحية"),
        ("POST", "/api/v2/social/schedule-post", "جدولة المنشورات"),
        ("GET", "/api/v2/social/inbox", "صندوق الوارد")
    ]
    
    passed = 0
    total = len(tests)
    
    for method, endpoint, description in tests:
        try:
            print(f"🧪 اختبار: {description}")
            
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}")
            elif method == "POST":
                # بيانات اختبار حسب نوع الـ endpoint
                if "comprehensive" in endpoint:
                    data = {
                        "brand": "شركة تجريبية",
                        "keywords": ["تسويق", "سيو"],
                        "timeframe": "30d"
                    }
                elif "keywords" in endpoint:
                    data = ["تسويق رقمي", "سيو"]
                elif "schedule-post" in endpoint:
                    data = {
                        "content": "منشور تجريبي",
                        "platforms": ["facebook", "twitter"]
                    }
                else:
                    data = {}
                    
                response = requests.post(f"{base_url}{endpoint}", json=data)
            
            if response.status_code == 200:
                print(f"   ✅ نجح ({response.status_code})")
                passed += 1
            else:
                print(f"   ❌ فشل ({response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  الخادم غير متاح على المنفذ 8001")
        except Exception as e:
            print(f"   ❌ خطأ: {e}")
            
        print("-" * 30)
    
    print(f"\n📊 النتائج:")
    print(f"✅ نجح: {passed}/{total}")
    print(f"❌ فشل: {total - passed}/{total}")
    print(f"📈 معدل النجاح: {(passed/total)*100:.1f}%")

def analyze_structure():
    """تحليل البنية الجديدة"""
    print("\n🏗️  تحليل البنية المعيارية:")
    print("=" * 40)
    
    structure = {
        "الملفات الأساسية": [
            "main_new.py - التطبيق الرئيسي المبسط",
            "config.py - الإعدادات والمتغيرات",
            "models.py - نماذج البيانات Pydantic",
            "agents.py - إدارة الوكلاء",
            "websocket_manager.py - إدارة WebSocket",
            "providers.py - مزودو البيانات (موجود مسبقاً)"
        ],
        "مجلد المسارات": [
            "routes/__init__.py",
            "routes/chat.py - مسارات المحادثة",
            "routes/analytics.py - مسارات التحليلات",
            "routes/social.py - مسارات وسائل التواصل",
            "routes/seo.py - مسارات السيو"
        ]
    }
    
    for category, files in structure.items():
        print(f"\n📁 {category}:")
        for file in files:
            print(f"   - {file}")
    
    print(f"\n🎯 الفوائد:")
    benefits = [
        "تنظيم أفضل للكود",
        "سهولة الصيانة والتطوير",
        "إمكانية العمل بفرق متعددة",
        "اختبار أسهل لكل وحدة",
        "قابلية إعادة الاستخدام",
        "تحسين الأداء"
    ]
    
    for benefit in benefits:
        print(f"   ✅ {benefit}")

if __name__ == "__main__":
    analyze_structure()
    print("\n" + "="*50)
    test_new_structure()
    
    print(f"\n📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 البنية الجديدة جاهزة للتطوير!")
