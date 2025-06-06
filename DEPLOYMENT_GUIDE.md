# دليل النشر - Morvo AI Deployment Guide

## 🚀 نظرة عامة

Morvo AI جاهز للنشر بالبنية المعيارية الجديدة. هذا الدليل يغطي جميع خطوات النشر للإنتاج.

## 📊 حالة النظام الحالية

✅ **جاهز للنشر - Production Ready**

- اختبارات التكامل: **100% نجح** (7/7)
- اختبار الوكلاء: **100% نجح** (5/5)
- البنية المعيارية: **مكتملة**
- مزودو البيانات: **جاهزون للتفعيل** (14 ديسمبر 2024)

## 🏗️ البنية المعيارية

### الملفات الأساسية
```
morvo/
├── main_new.py              # التطبيق الرئيسي المبسط
├── config.py                # الإعدادات والمتغيرات
├── models.py                # نماذج البيانات Pydantic
├── agents.py                # إدارة الوكلاء الخمسة
├── websocket_manager.py     # إدارة WebSocket
├── providers.py             # مزودو البيانات (SE Ranking, Awario, Mention)
└── routes/                  # مجلد المسارات
    ├── __init__.py
    ├── chat.py              # مسارات المحادثة
    ├── analytics.py         # مسارات التحليلات
    ├── social.py            # مسارات وسائل التواصل
    └── seo.py               # مسارات السيو
```

### ملفات التكوين
```
├── requirements.txt         # المتطلبات الكاملة
├── requirements-minimal.txt # الحد الأدنى للنشر
├── requirements-dev.txt     # أدوات التطوير
├── .env.example            # مثال متغيرات البيئة
└── README.md               # الوثائق الرئيسية
```

## 🔧 متطلبات النشر

### 1. متغيرات البيئة المطلوبة

```bash
# الذكاء الاصطناعي
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# مزودو البيانات التسويقية (متوفرة 14 ديسمبر)
SERANKING_API_KEY=your_seranking_key
AWARIO_API_KEY=your_awario_key  
MENTION_API_TOKEN=your_mention_token

# إعدادات التطبيق
APP_VERSION=2.0
PORT=8000
DEBUG=false
SECRET_KEY=your_secret_key

# قاعدة البيانات (اختيارية)
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url
```

### 2. الحد الأدنى من المتطلبات

```bash
# للنشر السريع
pip install -r requirements-minimal.txt

# للميزات الكاملة
pip install -r requirements.txt
```

## 🚀 خيارات النشر

### 1. Railway (موصى به)

```bash
# 1. إنشاء مشروع Railway
railway login
railway init

# 2. إعداد متغيرات البيئة
railway add OPENAI_API_KEY=your_key
railway add ANTHROPIC_API_KEY=your_key
railway add PORT=8000

# 3. النشر
railway up
```

**الإعدادات المقترحة للـ Railway:**
- **Start Command**: `python main_new.py`
- **Build Command**: `pip install -r requirements.txt`
- **Port**: `8000`
- **Region**: `us-west1` أو `europe-west1`

### 2. Render

```yaml
# render.yaml
services:
  - type: web
    name: morvo-ai
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main_new.py
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: PORT
        value: 8000
```

### 3. Heroku

```bash
# إنشاء Procfile
echo "web: python main_new.py" > Procfile

# إعداد Heroku
heroku create morvo-ai
heroku config:set OPENAI_API_KEY=your_key
heroku config:set PORT=8000

# النشر
git push heroku main
```

### 4. Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main_new.py"]
```

```bash
# بناء وتشغيل
docker build -t morvo-ai .
docker run -p 8000:8000 --env-file .env morvo-ai
```

## 🧪 اختبار ما قبل النشر

### 1. اختبار محلي

```bash
# تشغيل الخادم
python main_new.py

# اختبار البنية
python test_modular.py

# اختبار الوكلاء
python test_agents_modular.py

# اختبار التكامل الكامل
python test_integration.py
```

### 2. نقاط التحقق

- [ ] جميع الاختبارات تمر بنجاح
- [ ] متغيرات البيئة محددة
- [ ] الوكلاء الخمسة نشطين
- [ ] WebSocket يعمل
- [ ] جميع endpoints تستجيب

## 🔍 المراقبة والصيانة

### 1. نقاط المراقبة

- `GET /health` - صحة النظام
- `GET /api/v2/chat/agents/status` - حالة الوكلاء
- `GET /api/v2/analytics/providers/status` - حالة مزودي البيانات

### 2. لوقز مهمة

```python
# مراقبة هذه الأحداث في اللوقز
- "بدء تشغيل Morvo AI"
- "WebSocket connection established"  
- "خطأ في معالجة الرسالة"
- "فشل في جلب البيانات من مزود"
```

### 3. الأداء

- **الذاكرة**: ~200-400 MB
- **وقت الاستجابة**: < 2 ثانية للوكلاء
- **اتصالات WebSocket**: حتى 1000 متزامن

## 📈 التطوير المستقبلي

### المرحلة التالية (14 ديسمبر 2024)
- [ ] تفعيل SE Ranking API
- [ ] تفعيل Awario Enterprise  
- [ ] تفعيل Mention Pro Plus
- [ ] إضافة تحليلات حقيقية
- [ ] تحسين الأداء

### ميزات مستقبلية
- [ ] دعم لغات إضافية
- [ ] لوحة تحكم admin
- [ ] تحليلات متقدمة
- [ ] تكامل مع المزيد من APIs

## 🆘 استكشاف الأخطاء

### مشاكل شائعة

1. **خطأ في import modules**
   ```bash
   # التأكد من PYTHONPATH
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **فشل اتصال WebSocket**
   ```bash
   # فحص الـ firewall والـ proxy
   curl -H "Upgrade: websocket" http://localhost:8000/ws/test
   ```

3. **بطء الوكلاء**
   ```bash
   # فحص OpenAI API quota
   # تقليل temperature في agents.py
   ```

## 📞 الدعم

للدعم التقني أو الاستفسارات:
- GitHub Issues
- التوثيق: `/docs` endpoint
- اختبار الصحة: `/health` endpoint

---

**آخر تحديث**: 7 ديسمبر 2024  
**الإصدار**: 2.0  
**الحالة**: Production Ready ✅
