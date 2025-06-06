# Morvo AI - مساعد التسويق الذكي 🤖

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/morvo-ai)
[![Production Ready](https://img.shields.io/badge/status-production%20ready-green.svg)](https://morvo.ai)
[![Tests](https://img.shields.io/badge/tests-passing%20100%25-brightgreen.svg)](tests/)

## 🚀 نظرة عامة

**Morvo AI** هو مساعد التسويق الذكي الأكثر تطوراً في المنطقة، مدعوم بـ 5 وكلاء متخصصين يقدمون تحليلات عميقة ورؤى قابلة للتنفيذ في مجال التسويق الرقمي.

### ✨ المزايا الرئيسية

- **5 وكلاء متخصصين** مع كشف النوايا التلقائي
- **تحليلات متقدمة** للسوق والمنافسين
- **مراقبة وسائل التواصل** في الوقت الفعلي
- **تحسين الحملات** الإعلانية وعائد الاستثمار
- **استراتيجيات المحتوى** الإبداعية
- **تحليل البيانات** التسويقية المتقدم

## 🏗️ البنية المعيارية

```
morvo/
├── main_new.py                 # التطبيق الرئيسي (133 سطر)
├── agents.py                   # إدارة الوكلاء الخمسة
├── websocket_manager.py        # إدارة WebSocket
├── config.py                   # إعدادات النظام
├── models.py                   # نماذج البيانات
├── providers.py                # مزودو البيانات التسويقية
├── routes/                     # مجلد المسارات المعيارية
│   ├── chat.py                 # مسارات المحادثة
│   ├── analytics.py            # مسارات التحليلات
│   ├── social.py               # مسارات وسائل التواصل
│   └── seo.py                  # مسارات السيو
├── requirements.txt            # المتطلبات الأساسية
├── DEPLOYMENT_GUIDE.md         # دليل النشر
└── tests/                      # اختبارات شاملة
```

## 🤖 الوكلاء المتخصصون

### M1 - محلل استراتيجي متقدم
- تحليل السوق والمنافسين
- التوصيات الاستراتيجية
- دراسات الجدوى

### M2 - مراقب وسائل التواصل الاجتماعي  
- مراقبة المنصات الاجتماعية
- تحليل التفاعل والإشارات
- إدارة السمعة الرقمية

### M3 - محسن الحملات التسويقية
- تحليل أداء الحملات
- تحسين عائد الاستثمار
- إدارة الميزانيات

### M4 - استراتيجي المحتوى الإبداعي
- تطوير استراتيجيات المحتوى
- التقويم الإبداعي
- تحسين التفاعل

### M5 - محلل البيانات التسويقية المتقدم
- تحليل البيانات المعقدة
- التنبؤات التسويقية
- تقارير الأداء

## 🚀 التشغيل السريع

### المتطلبات
- Python 3.8+
- مفاتيح API (OpenAI, Anthropic)

### التثبيت
```bash
# استنسخ المشروع
git clone https://github.com/your-repo/morvo-ai.git
cd morvo-ai

# ثبت المتطلبات
pip install -r requirements.txt

# إعداد متغيرات البيئة
cp .env.example .env
# أدخل مفاتيح API في ملف .env

# تشغيل التطبيق
python main_new.py
```

### أو استخدم سكربت البدء:
```bash
chmod +x start.sh
./start.sh
```

## 🧪 الاختبارات

```bash
# اختبار البنية المعيارية
python test_modular.py

# اختبار الوكلاء
python test_agents_modular.py

# اختبار التكامل الشامل
python test_integration.py
```

## 📊 حالة النظام

- **الحالة**: ✅ Production Ready
- **الإصدار**: 2.0
- **الاختبارات**: 19/19 نجح (100%)
- **الوكلاء**: 5/5 نشط
- **WebSocket**: يدعم 1000+ اتصال متزامن

## 🌐 النشر

### Railway (موصى به)
```bash
railway login
railway init
railway deploy
```

### Docker
```bash
docker build -t morvo-ai .
docker run -p 8000:8000 morvo-ai
```

### Render/Heroku
اتبع `DEPLOYMENT_GUIDE.md` للتعليمات المفصلة.

## 🔮 المستقبل القريب

### 14 ديسمبر 2024 - تفعيل مزودي البيانات:
- **SE Ranking**: تحليل SEO ومراقبة الكلمات
- **Awario**: مراقبة الإشارات والعلامة التجارية  
- **Mention**: إدارة وسائل التواصل الموحدة

## 📡 API Endpoints

```
GET  /                          # الصفحة الرئيسية
GET  /health                    # فحص الصحة
POST /api/v2/chat/message       # إرسال رسالة للوكلاء
GET  /api/v2/providers/status   # حالة مزودي البيانات
POST /api/v2/analytics/comprehensive  # التحليل الشامل
POST /api/v2/seo/keywords       # تحليل الكلمات المفتاحية
POST /api/v2/social/schedule    # جدولة المنشورات
GET  /api/v2/social/inbox       # صندوق الوارد
WS   /ws                        # اتصال WebSocket
```

## 🔒 الأمان

- مصادقة JWT
- تشفير البيانات
- معدل طلبات محدود
- متغيرات بيئة آمنة

## 📞 الدعم

- **التوثيق**: [docs.morvo.ai](https://docs.morvo.ai)
- **المجتمع**: [discord.gg/morvo](https://discord.gg/morvo)
- **البريد**: support@morvo.ai

---

**Morvo AI** - *من فكرة إلى منتج جاهز للنشر* 🚀

*تم التطوير بواسطة Cascade AI*
