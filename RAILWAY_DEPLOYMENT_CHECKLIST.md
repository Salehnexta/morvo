# 🚀 Railway Deployment Checklist - Morvo AI Enhanced

## ✅ Pre-Deployment Requirements

### 📁 **Required Files**
- [x] `main.py` - Enhanced FastAPI application with MCP/A2A
- [x] `agents.py` - Enhanced agents with MCP and A2A protocols  
- [x] `protocols.py` - Protocol manager for MCP/A2A coordination
- [x] `config.py` - Enhanced configuration with protocol settings
- [x] `requirements.txt` - Updated dependencies (httpx, aiofiles)
- [x] `railway.toml` - Enhanced Railway configuration
- [x] `deploy-railway.sh` - Automated deployment script

### 🔧 **Environment Variables Required**

#### Core Application
```bash
# Basic FastAPI settings
PORT=8000
HOST=0.0.0.0

# Enhanced Protocol Configuration  
ENHANCED_PROTOCOLS_AVAILABLE=true
MCP_ENABLED=true
A2A_ENABLED=true

# Performance Tuning
UVICORN_WORKERS=2
UVICORN_TIMEOUT_KEEP_ALIVE=30
UVICORN_MAX_REQUESTS=1000
ASYNCIO_TIMEOUT=60

# Logging
LOG_LEVEL=INFO
ENABLE_PROTOCOL_LOGGING=true
```

#### Required API Keys
```bash
# OpenAI for enhanced agents
OPENAI_API_KEY=sk-...

# Supabase for MCP data sources
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_ACCESS_TOKEN=sbp_...

# JWT for authentication
JWT_SECRET_KEY=your-secret-key

# Optional: Social media monitoring
AWARIO_API_KEY=your-awario-key
MENTION_API_KEY=your-mention-key
```

## 🚀 **Deployment Steps**

### 1. **Prepare Environment**
```bash
# Install Railway CLI (if not installed)
npm install -g @railway/cli

# Login to Railway
railway login

# Verify current directory
pwd  # Should be /Users/salehgazwani/Documents/morvo
```

### 2. **Run Automated Deployment**
```bash
# Execute deployment script
./deploy-railway.sh
```

**OR Manual Deployment:**

### 3. **Manual Railway Setup**
```bash
# Create/connect to Railway project
railway link

# Set environment variables
railway variables set ENHANCED_PROTOCOLS_AVAILABLE=true
railway variables set MCP_ENABLED=true
railway variables set A2A_ENABLED=true
railway variables set OPENAI_API_KEY=your-key
railway variables set SUPABASE_URL=your-url
railway variables set SUPABASE_KEY=your-key

# Deploy
railway up
```

## 🔍 **Post-Deployment Verification**

### Health Checks
1. **Basic Health**: `https://your-app.railway.app/health`
2. **Detailed Health**: `https://your-app.railway.app/health/detailed`  
3. **Protocol Status**: `https://your-app.railway.app/protocols/status`

### Enhanced Features Testing
1. **MCP Resources**: `https://your-app.railway.app/mcp/resources`
2. **A2A Network**: `https://your-app.railway.app/a2a/network`
3. **WebSocket**: Test chat functionality
4. **Agent Status**: Verify all 5 agents are active

### Expected Response Examples

#### `/health/detailed`
```json
{
  "status": "healthy",
  "timestamp": "2025-06-07T12:46:00Z",
  "version": "2.1.0",
  "protocols": {
    "mcp_enabled": true,
    "a2a_enabled": true,
    "enhanced_agents": true
  },
  "agents_count": 5,
  "uptime": "120 seconds"
}
```

#### `/protocols/status`
```json
{
  "mcp_status": "active",
  "a2a_status": "active", 
  "initialization_complete": true,
  "enhanced_agents_available": true,
  "agents_count": 5
}
```

## 🛠️ **Troubleshooting**

### Common Issues & Solutions

#### 1. **Protocol Initialization Errors**
```bash
# Check logs
railway logs

# Verify environment variables
railway variables
```

#### 2. **Agent Loading Issues**
- Verify `OPENAI_API_KEY` is set
- Check `SUPABASE_*` variables for MCP data access
- Ensure `protocols.py` is properly deployed

#### 3. **Performance Issues**
- Monitor resource usage: `railway metrics`
- Adjust `UVICORN_WORKERS` if needed
- Check `ASYNCIO_TIMEOUT` settings

#### 4. **MCP Resource Access**
- Verify Supabase credentials
- Check database table permissions
- Test MCP resource endpoints manually

## 📈 **Enhanced Features Available**

### ✅ **What's New in This Deployment**
1. **MCP Protocol**: Real-time data access from Supabase
2. **A2A Communication**: Inter-agent collaboration 
3. **Enhanced Agents**: 5 specialized AI agents with protocols
4. **Protocol Manager**: Centralized protocol coordination
5. **Performance Tuning**: Optimized for Railway environment
6. **Advanced Health Checks**: Detailed system monitoring

### 🎯 **Integration Ready For**
- Dashboard + Chat companion hybrid approach
- Real-time Supabase data integration  
- Multi-agent collaborative processing
- Context-aware conversational AI
- Gulf-friendly tone and responses

## 🔄 **Continuous Deployment**

### Auto-Deploy Setup
```bash
# Connect GitHub repository (optional)
railway connect

# Enable auto-deploy on git push
railway environments
```

### Monitoring & Logs
```bash
# View real-time logs
railway logs --follow

# Check deployment status
railway status

# View metrics
railway metrics
```

---

## ✅ **Deployment Complete!**

Once deployed successfully, your enhanced Morvo AI platform will have:

🤖 **5 Enhanced AI Agents** with MCP & A2A protocols  
📊 **Real-time Supabase integration** via MCP resources  
🔄 **Inter-agent collaboration** via A2A communication  
🚀 **Optimized Railway performance** with proper scaling  
🌐 **Ready for hybrid dashboard + chat** integration  

**Next Step**: Test the deployment and integrate with your frontend! 🎉
