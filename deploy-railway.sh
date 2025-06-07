#!/bin/bash

# 🚀 Enhanced Railway Deployment Script for Morvo AI
# مع دعم بروتوكولات MCP و A2A المحسنة

echo "🚀 بدء نشر Morvo AI Enhanced على Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI غير مثبت. يرجى تثبيته أولاً:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Check if logged in to Railway
if ! railway status &> /dev/null; then
    echo "🔐 يرجى تسجيل الدخول إلى Railway:"
    railway login
fi

echo "📋 فحص الملفات المطلوبة..."

# Check required files
REQUIRED_FILES=(
    "main.py"
    "agents.py"
    "protocols.py"
    "config.py"
    "requirements.txt"
    "railway.toml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ ملف مطلوب مفقود: $file"
        exit 1
    fi
    echo "✅ $file موجود"
done

echo "🔧 فحص متغيرات البيئة المطلوبة..."

# Set enhanced environment variables
echo "⚙️ تكوين متغيرات البيئة المحسنة..."

# Protocol configuration
railway variables set ENHANCED_PROTOCOLS_AVAILABLE=true
railway variables set MCP_ENABLED=true  
railway variables set A2A_ENABLED=true

# Performance tuning
railway variables set UVICORN_WORKERS=2
railway variables set UVICORN_TIMEOUT_KEEP_ALIVE=30
railway variables set UVICORN_MAX_REQUESTS=1000
railway variables set ASYNCIO_TIMEOUT=60

# Logging
railway variables set LOG_LEVEL=INFO
railway variables set ENABLE_PROTOCOL_LOGGING=true

echo "📦 نشر التطبيق المحسن..."

# Deploy with enhanced configuration
railway up --detach

echo "🔍 فحص حالة النشر..."
railway status

echo "📊 رابط التطبيق:"
railway domain

echo "✅ تم نشر Morvo AI Enhanced بنجاح!"
echo "🔄 البروتوكولات المتاحة: MCP + A2A"
echo "🤖 الوكلاء المحسنون: 5 وكلاء ذكيين"
echo "📈 مع دعم الذكاء الاصطناعي المتقدم"

echo ""
echo "🔗 للوصول إلى التطبيق:"
echo "   - الصحة العامة: /health"
echo "   - الصحة المفصلة: /health/detailed"  
echo "   - حالة البروتوكولات: /protocols/status"
echo "   - موارد MCP: /mcp/resources"
echo "   - شبكة A2A: /a2a/network"
