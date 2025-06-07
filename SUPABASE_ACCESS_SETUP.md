# 🔑 Supabase MCP Access Token Setup

## المشكلة الحالية:
- MCP Supabase يحتاج **Personal Access Token** وليس API keys
- لدينا API Keys ولكن نحتاج Personal Access Token مختلف

## 📋 الخطوات المطلوبة:

### 1. احصل على Personal Access Token:
```
🔗 اذهب إلى: https://supabase.com/dashboard/account/tokens
👤 سجل دخول بحساب Supabase
➕ اضغط "Generate new token"
📝 اختر الصلاحيات المطلوبة:
   ✅ projects:read
   ✅ projects:write
   ✅ organizations:read
📋 انسخ التوكن (مثال: sbp_xxxxx...)
```

### 2. ضع التوكن في Environment Variables:
```bash
# في Railway Dashboard - Environment Variables
SUPABASE_ACCESS_TOKEN=sbp_your_personal_access_token_here

# أو محلياً للتطوير
export SUPABASE_ACCESS_TOKEN="sbp_your_personal_access_token_here"
```

### 3. اختبر الاتصال:
```bash
# سيتم اختبار الاتصال بعد إعداد التوكن
```

## 🔍 معلومات إضافية:

**الفرق بين التوكنات:**
- **API Key (anon)**: للتطبيقات والـ frontend
- **Service Role Key**: للـ backend operations
- **Personal Access Token**: لـ MCP وإدارة المشاريع

**المشروع الحالي:**
- Project ID: `teniefzxdikestahndur`
- URL: `https://teniefzxdikestahndur.supabase.co`

## ⏭️ بعد الحصول على التوكن:
1. ضع التوكن في Environment Variables
2. سأستخدم MCP للوصول إلى الجداول
3. سأراجع الجداول الموجودة
4. سأطبق التحديثات المطلوبة
