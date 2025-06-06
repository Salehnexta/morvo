# 🚀 دليل نشر Morvo AI على Railway

## الحالة الحالية ✅
- **البنية المعيارية**: مُحدثة بالكامل (main_new.py + agents.py + routes/)
- **التبعيات**: تم حل جميع التضاربات (requirements.txt خالي من الأخطاء)
- **الإعدادات**: railway.toml و .railwayignore محدثان
- **GitHub**: جميع الملفات مرفوعة ومزامنة

## خطوات النشر على Railway 🛤️

### 1. الدخول لـ Railway
```
الذهاب إلى: https://railway.app/
تسجيل الدخول أو إنشاء حساب جديد
```

### 2. إنشاء مشروع جديد
```
1. اضغط على "New Project"
2. اختر "Deploy from GitHub repo"
3. اختر مستودع: Salehnexta/morvo
4. سيبدأ النشر تلقائياً
```

### 3. إعداد متغيرات البيئة 🔐
في لوحة Railway، اذهب لـ Variables واضف:

```env
OPENAI_API_KEY=your_openai_api_key_here
PORT=8000
APP_VERSION=2.0.0
PYTHONPATH=/app
RAILWAY_STATIC_URL=/static
```

### 4. التحقق من النشر ✅
- انتظر انتهاء عملية البناء (Building)
- تحقق من الـ logs للتأكد من عدم وجود أخطاء
- اختبر الرابط المُولد تلقائياً

## الملفات الأساسية للنشر 📁

### Core Files ✅
- `main_new.py` - التطبيق الرئيسي
- `agents.py` - نظام الوكلاء الخمسة
- `websocket_manager.py` - إدارة WebSocket
- `routes/` - جميع مسارات API

### Configuration ✅
- `requirements.txt` - التبعيات المُحدثة (بدون تضاربات)
- `railway.toml` - إعدادات Railway
- `.railwayignore` - ملفات مستبعدة من النشر

## اختبار النشر 🧪

### 1. صحة الخادم
```bash
curl https://your-app.railway.app/health
# يجب أن يعيد: {"status": "healthy", "agents": 5}
```

### 2. اختبار الوكلاء
```bash
curl -X POST https://your-app.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "تحليل السوق للمنتج الجديد"}'
```

### 3. WebSocket
```javascript
const ws = new WebSocket('wss://your-app.railway.app/ws');
ws.onopen = () => console.log('WebSocket connected');
```

## استكشاف الأخطاء 🔍

### مشاكل شائعة:

1. **Build Failed**
   - تحقق من logs في Railway
   - تأكد من وجود جميع الملفات في GitHub

2. **Import Errors**
   - تحقق من `PYTHONPATH` في متغيرات البيئة
   - تأكد من البنية المعيارية صحيحة

3. **API Key Missing**
   - تحقق من `OPENAI_API_KEY` في Variables
   - تأكد من صحة المفتاح

## المميزات المُفعلة بعد النشر 🌟

### الوكلاء الخمسة:
- **M1**: محلل استراتيجي متقدم
- **M2**: مراقب وسائل التواصل
- **M3**: محسن الحملات التسويقية  
- **M4**: استراتيجي المحتوى
- **M5**: محلل البيانات التسويقية

### API Endpoints:
- `/health` - فحص صحة الخادم
- `/api/chat` - محادثة مع الوكلاء
- `/api/analytics` - تحليلات التسويق
- `/api/social` - وسائل التواصل
- `/api/seo` - تحسين محركات البحث
- `/ws` - WebSocket للاتصال المباشر

## ملاحظات مهمة ⚠️

1. **الأمان**: جميع API keys محمية في متغيرات البيئة
2. **الأداء**: البنية المعيارية تحسن الذاكرة والسرعة
3. **التوسع**: يمكن إضافة وكلاء جدد بسهولة
4. **المراقبة**: Railway يوفر logs ومراقبة تلقائية

## الدعم والصيانة 🛠️

- **التحديثات**: git push يحدث النشر تلقائياً
- **المراقبة**: لوحة Railway تعرض الحالة والإحصائيات
- **النسخ الاحتياطي**: GitHub يحفظ جميع الإصدارات

---

**✅ المشروع جاهز للنشر الفوري على Railway**

التاريخ: 7 يناير 2025  
الإصدار: 2.0.0 (البنية المعيارية)
