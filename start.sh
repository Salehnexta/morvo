#!/bin/bash
# Morvo AI Startup Script

echo "🚀 بدء تشغيل Morvo AI..."

# فحص متغيرات البيئة المطلوبة
required_vars=("OPENAI_API_KEY")

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ متغير البيئة مفقود: $var"
        echo "💡 تأكد من إعداد ملف .env"
        exit 1
    fi
done

# تثبيت المتطلبات إذا لم تكن موجودة
if [ ! -d "venv" ]; then
    echo "🔧 إنشاء البيئة الافتراضية..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ البيئة الافتراضية موجودة"
    source venv/bin/activate
fi

# تشغيل التطبيق
echo "🌟 تشغيل Morvo AI بالبنية المعيارية..."
python main_new.py
