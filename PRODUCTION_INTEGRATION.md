# Morvo AI Production Integration Guide

## Production Environment
**Production URL**: https://morvo-production.up.railway.app

This document provides guidance on integrating with the Morvo AI production environment.

## Endpoints

### Core Endpoints
- **Health Check**: `GET /health` - Basic health status
- **Detailed Health**: `GET /health/detailed` - Comprehensive system status
- **Chat API**: `POST /chat` - Send messages to Morvo AI
- **WebSocket**: `WSS /ws/{user_id}` - Real-time chat connection

### Agent Interaction
All interactions are now handled through the unified "مورفو" conversational companion, which internally coordinates with the 5 specialized agents:
- محلل استراتيجي متقدم (Strategic Analyst)
- مراقب وسائل التواصل (Social Media Monitor)
- محسن الحملات (Campaign Optimizer)
- استراتيجي المحتوى (Content Strategist)
- محلل البيانات (Data Analyst)

## Integration Methods

### Method 1: Direct API Integration
```javascript
// Example API call to chat endpoint
const response = await fetch('https://morvo-production.up.railway.app/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'أريد تحسين استراتيجية التسويق الخاصة بي',
    user_id: 'user-123',
    context: {
      business_type: 'ecommerce',
      language: 'arabic'
    }
  })
});

const data = await response.json();
```

### Method 2: WebSocket Integration (Real-time Chat)
```javascript
// Example WebSocket connection
const socket = new WebSocket(`wss://morvo-production.up.railway.app/ws/user-123`);

socket.onopen = () => {
  console.log('Connected to Morvo AI');
  socket.send(JSON.stringify({
    type: 'message',
    content: 'مرحبًا مورفو',
    user_id: 'user-123'
  }));
};

socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Message from Morvo:', message.content);
};
```

### Method 3: React Component Integration
```javascript
// Example React component using Morvo AI Chat
import { MorvoChat } from '@morvo/react-components';

function App() {
  return (
    <div className="app">
      <header>My Dashboard</header>
      <main>
        {/* Your dashboard content */}
      </main>
      <MorvoChat 
        apiUrl="https://morvo-production.up.railway.app"
        userId="user-123"
        language="ar"
        theme="light"
        position="bottom-right"
      />
    </div>
  );
}
```

## Authentication
Include your API key in the headers for authenticated requests:

```javascript
headers: {
  'Content-Type': 'application/json',
  'X-API-Key': 'your_api_key_here'
}
```

## Best Practices
1. **Error Handling**: Implement proper error handling for all API calls
2. **Rate Limiting**: Respect the rate limits (100 requests per minute)
3. **Timeout Handling**: Set appropriate timeouts for requests (recommended: 30s)
4. **Fallback Mechanism**: Have fallbacks in case of service disruption

## Testing
Use the following test user IDs for development:
- `test-user-1` - Basic user profile
- `test-user-2` - Complete user profile with business data

## Need Help?
Refer to the complete API documentation or contact support for assistance.
