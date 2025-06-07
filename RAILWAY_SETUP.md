# 🚀 Railway Setup for Morvo AI with Supabase

## Architecture Overview
- **Frontend**: Lovable React (existing repo)
- **Backend/Database**: Supabase (configured)
- **API Server**: FastAPI + CrewAI agents (Railway)
- **Agents**: 5 specialized agents (M1-M5)

## Current Railway Service
- **URL**: https://morvo-production.up.railway.app
- **Service**: adaptable-optimism
- **Status**: Building/Deploying

## Required Environment Variables

Add these to Railway Dashboard → Variables:

```bash
# Supabase Configuration (Primary Database)
SUPABASE_URL=https://teniefzxdikestahndur.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlbmllZnp4ZGlrZXN0YWhkbnVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg2MjI2NTIsImV4cCI6MjA2NDE5ODY1Mn0.k5eor_-j2aTheb1q6OhGK8DWGjucRWK11eFAOpAZP3I

# API Keys
RAPIDAPI_KEY=df76b9a44emshdfe1a42c0a600ffp192615jsn9f5f9489bf3b

# Security
JWT_SECRET_KEY=morvo-ai-enhanced-secret-key-2025-production
DEBUG=false

# Optional: For chat functionality
# OPENAI_API_KEY=your_openai_key_here
```

## Service Configuration
- **Start Command**: `python main.py`
- **Health Check**: `/health`
- **Port**: Auto-detected
- **Build**: Nixpacks (Python)

## Next Steps
1. Add environment variables to Railway
2. Trigger redeploy
3. Test API endpoints
4. Connect React frontend to Railway API
5. Test all 5 agents functionality

## API Endpoints to Test
- GET `/health` - Service health
- GET `/api/v2/chat/agents/status` - Agents status
- POST `/api/v2/seo/audit` - SEO audit (RapidAPI)
- GET `/api/v2/analytics/providers/status` - Analytics
- WebSocket `/ws/{user_id}` - Real-time communication
