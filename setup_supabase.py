#!/usr/bin/env python3
"""
Supabase Setup and Configuration Script for Morvo AI
This script helps configure Supabase as the primary database.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY, DATABASE_URL

def main():
    print("🔍 **SUPABASE CONFIGURATION STATUS**\n")
    
    # Check current configuration
    print("📋 **Current Configuration:**")
    print(f"SUPABASE_URL: {SUPABASE_URL[:50]}..." if SUPABASE_URL else "❌ SUPABASE_URL: Not set")
    print(f"SUPABASE_KEY: {SUPABASE_KEY[:50]}..." if SUPABASE_KEY else "❌ SUPABASE_KEY: Not set")
    
    if SUPABASE_SERVICE_ROLE_KEY and SUPABASE_SERVICE_ROLE_KEY != '"YOUR_SERVICE_ROLE_KEY_HERE"  # Get this from Supabase Dashboard → Settings → API':
        print(f"SUPABASE_SERVICE_ROLE_KEY: {SUPABASE_SERVICE_ROLE_KEY[:50]}...")
        print(f"✅ Generated DATABASE_URL: {DATABASE_URL[:50]}..." if DATABASE_URL else "❌ DATABASE_URL: Failed to generate")
    else:
        print("❌ SUPABASE_SERVICE_ROLE_KEY: Not set properly")
        print("\n🔑 **TO FIX THIS:**")
        print("1. Go to your Supabase Dashboard: https://app.supabase.com/")
        print("2. Select your project: teniefzxdikestahndur")
        print("3. Go to Settings → API")
        print("4. Copy the 'service_role' key (not the 'anon' key)")
        print("5. Set it as environment variable:")
        print("   export SUPABASE_SERVICE_ROLE_KEY='your_actual_service_role_key'")
    
    print("\n🎯 **CURRENT DATABASE PRIORITY:**")
    if DATABASE_URL and "supabase.co" in DATABASE_URL:
        print("✅ Using Supabase as primary database")
    elif DATABASE_URL and "railway.app" in DATABASE_URL:
        print("⚠️  Using Railway Postgres (should use Supabase instead)")
    elif DATABASE_URL:
        print(f"ℹ️  Using custom database: {DATABASE_URL[:50]}...")
    else:
        print("❌ No database configured")
    
    print("\n🚀 **RECOMMENDATIONS:**")
    if not DATABASE_URL or "railway.app" in DATABASE_URL:
        print("1. Set up Supabase Service Role Key to use Supabase database")
        print("2. Remove Railway Postgres dependency")
        print("3. Update environment variables in Railway deployment")
    else:
        print("✅ Configuration looks good! Supabase is ready to use.")
    
    print("\n📊 **NEXT STEPS:**")
    print("1. Set SUPABASE_SERVICE_ROLE_KEY environment variable")
    print("2. Run: python setup_supabase.py (this script) to verify")
    print("3. Deploy to Railway with updated environment variables")
    print("4. Test all endpoints with Supabase backend")

if __name__ == "__main__":
    main()
