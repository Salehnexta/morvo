# 🤖 Morvo AI - Enhanced Edition

> **Advanced AI Marketing Assistant with CrewAI Multi-Agent System**

![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-teal.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-0.74.0-orange.svg)
![Deploy](https://img.shields.io/badge/deploy-Railway-purple.svg)

## ✨ **المميزات الأساسية**

### 🎯 **نظام وكلاء متعدد (Multi-Agent System)**
- **محلل تسويق رقمي خبير:** تحليل البيانات والسوق بدقة
- **منشئ محتوى إبداعي:** إنشاء محتوى مناسب للثقافة العربية  
- **معالج ذكي:** توجيه تلقائي للطلبات حسب التخصص

### 🔧 **التقنيات المتقدمة**
- **FastAPI:** أداء عالي وتوثيق تلقائي
- **WebSocket:** محادثة فورية وتفاعلية
- **CrewAI:** نظام وكلاء ذكي مدعوم بـ GPT-4
- **Arabic Support:** دعم كامل للغة العربية
- **Fallback System:** يعمل بدون مفتاح OpenAI

## 🚀 **النشر على Railway**

### المتطلبات الأساسية
```bash
# 1. استنساخ المستودع
git clone https://github.com/Salehnexta/morvo.git
cd morvo

# 2. تثبيت المتطلبات (للتطوير المحلي)
pip install -r requirements.txt

# 3. إعداد متغيرات البيئة
cp .env.example .env
# أضف OPENAI_API_KEY إلى .env
```

### ⚙️ **إعداد Railway**
1. **ربط المستودع:** اربط `github.com/Salehnexta/morvo` بـ Railway
2. **Nixpacks Automatic:** Railway سيستخدم Nixpacks تلقائياً
3. **Environment Variables:**
   ```
   OPENAI_API_KEY=your_key_here
   ```
4. **النشر التلقائي:** كل `git push` ينشر التحديثات

### 🔗 **النقاط النهائية (Endpoints)**

| النقطة | الوصف |
|--------|--------|
| `GET /` | معلومات الخدمة |
| `GET /health` | فحص صحة النظام |
| `POST /api/v2/chat/message` | API المحادثة |
| `WS /ws/{user_id}` | WebSocket |

## 💬 **استخدام المحادثة**

### 🔹 **مع مفتاح OpenAI (CrewAI مُفعل)**
```bash
"أريد تحليل موقعي الإلكتروني"
"اكتب لي منشور لوسائل التواصل الاجتماعي"
"ضع لي استراتيجية تسويق رقمي للمتجر"
```

### 🔹 **بدون مفتاح OpenAI (النظام البسيط)**
```bash
"مرحبا"
"مساعدة"
"كيف يمكنني البدء؟"
```

## 📁 **هيكل المشروع**

```
morvo/
├── main.py                # التطبيق الرئيسي
├── requirements.txt       # المتطلبات
├── railway.toml          # إعدادات Railway
├── .railwayignore        # ملفات مستبعدة من النشر
├── .env                  # متغيرات البيئة
├── .env.example          # مثال على متغيرات البيئة
├── .gitignore           # ملفات مستبعدة من Git
└── README.md            # هذا الملف
```

## 🔧 **التطوير المحلي**

```bash
# تشغيل الخادم محلياً
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# اختبار الصحة
curl http://localhost:8000/health

# اختبار المحادثة
curl -X POST http://localhost:8000/api/v2/chat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "مرحبا", "user_id": "test_user"}'
```

---

**🚀 مورفو - مساعدك الذكي في التسويق الرقمي**  
*مدعوم بتقنيات الذكاء الاصطناعي المتقدمة*
