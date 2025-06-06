"""
Morvo AI - Main Application (Updated to Modular Architecture)
This file now redirects to the new modular structure.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("🚀 تشغيل Morvo AI بالبنية المعيارية الجديدة...")
print("📁 استخدام: main_new.py")

# Import and run the new modular application
try:
    from main_new import app
    print("✅ تم تحميل البنية الجديدة بنجاح")
    
    if __name__ == "__main__":
        import uvicorn
        print("🌟 بدء تشغيل Morvo AI...")
        uvicorn.run("main_new:app", host="0.0.0.0", port=8000, reload=False)
        
except ImportError as e:
    print(f"❌ خطأ في تحميل البنية الجديدة: {e}")
    print("💡 تأكد من وجود جميع الملفات المطلوبة")
    sys.exit(1)
