# مورفو (Morvo) - Unified Companion Deployment Guide

This guide outlines the deployment steps for the unified "مورفو" conversational marketing companion.

## Overview

The Morvo unified companion ("مورفو") replaces the previous multi-agent system with a single, powerful conversational marketing assistant that provides Gulf-friendly Arabic responses focused on business KPIs and marketing insights.

## Deployment Steps

### 1. Deploy Database Schema

First, deploy the required database tables to your Supabase project:

```bash
# Deploy the prompts table
psql -h db.teniefzxdikestahndur.supabase.co -U postgres -d postgres -f migrations/01_create_prompts_table.sql

# Deploy the MCP tables (agent memories, cross-agent context)
psql -h db.teniefzxdikestahndur.supabase.co -U postgres -d postgres -f migrations/02_create_mcp_tables.sql
```

Alternatively, you can copy-paste the SQL directly into the Supabase SQL Editor in the Dashboard.

### 2. Deploy Edge Function

Deploy the Supabase Edge Function for the unified companion:

```bash
# Navigate to the project root
cd /Users/salehgazwani/Documents/morvo

# Set necessary environment variables (copy from example)
cp supabase/functions/unified-companion/.env.example supabase/functions/.env.production
# Edit the .env.production file with your actual values

# Deploy the Edge Function
supabase functions deploy unified-companion --project-ref teniefzxdikestahndur
```

### 3. Test the Edge Function

```bash
# Test with curl
curl -X POST "https://teniefzxdikestahndur.supabase.co/functions/v1/unified-companion" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [YOUR_SUPABASE_ANON_KEY]" \
  -d '{"message": "مرحبا", "user_id": "test-user-1"}'
```

### 4. Test with Demo UI

Open the demo UI in your browser to test the companion:

```bash
# Start a simple HTTP server
cd /Users/salehgazwani/Documents/morvo/demo
python3 -m http.server 8000
```

Then visit [http://localhost:8000/unified-companion-test.html](http://localhost:8000/unified-companion-test.html) in your browser.

## Production Integration

### Frontend React Integration

Here's a simplified React component for integrating the unified companion:

```jsx
import { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://your-project-id.supabase.co';
const supabaseAnonKey = 'your-anon-key';
const supabase = createClient(supabaseUrl, supabaseAnonKey);

function MorvoCompanion() {
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const sendMessage = async () => {
    if (!message.trim()) return;
    
    // Add user message to conversation
    setConversation(prev => [...prev, { role: 'user', content: message }]);
    setIsLoading(true);
    
    try {
      const { data, error } = await supabase.functions.invoke('unified-companion', {
        body: {
          message: message,
          user_id: 'current-user-id', // Replace with actual user ID
          conversation_id: conversationId
        }
      });
      
      if (error) throw error;
      
      // Add assistant response
      setConversation(prev => [...prev, { role: 'assistant', content: data.response }]);
      
      // Save conversation ID for continuation
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }
    } catch (error) {
      console.error('Error calling Morvo companion:', error);
    } finally {
      setIsLoading(false);
      setMessage('');
    }
  };
  
  return (
    <div className="morvo-companion">
      <div className="morvo-conversation">
        {conversation.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {isLoading && <div className="loading">مورفو يكتب...</div>}
      </div>
      
      <div className="morvo-input">
        <input 
          value={message} 
          onChange={e => setMessage(e.target.value)}
          placeholder="اكتب رسالتك لمورفو..."
          disabled={isLoading}
        />
        <button onClick={sendMessage} disabled={isLoading || !message.trim()}>
          إرسال
        </button>
      </div>
    </div>
  );
}

export default MorvoCompanion;
```

### REST API Endpoint

You can also access the unified companion directly via REST API:

- **Endpoint**: `https://teniefzxdikestahndur.supabase.co/functions/v1/unified-companion` 
- **Method**: POST
- **Headers**:
  - Content-Type: application/json
  - Authorization: Bearer [YOUR_SUPABASE_ANON_KEY]
- **Body**:
  ```json
  {
    "message": "مرحبا مورفو، كيف يمكنني تحسين حملتي التسويقية؟",
    "user_id": "your-user-id",
    "conversation_id": "optional-conversation-id",
    "context": {
      "business_type": "ecommerce",
      "language": "arabic"
    }
  }
  ```

## Monitoring and Updates

### System Prompt Updates

To update the system prompt:

1. Access your Supabase Dashboard
2. Navigate to the SQL Editor
3. Run a query to update the prompt:


```sql
UPDATE prompts
SET content = 'أنت «مورفو» – رفيق تسويق ذكي واحد.
• تحدّث بالعربية الفصحى بلمسة خليجية ودودة.
• وظيفتك تبسيط التسويق: تحليل SEO، أفكار محتوى، حملات، تتبّع ROI.
• جمَل قصيرة، أفعال مباشرة، إيموجي واحد كحدّ أقصى.
• لا تتجاوز 300 كلمة في أي ردّ.',
version = version + 1,
updated_at = now()
WHERE name = 'morvo_unified_companion' AND is_active = true;
```

### Monitoring

Monitor the unified companion performance using:

1. Supabase Dashboard (Edge Function logs)
2. Railway production logs: [https://morvo-production.up.railway.app/health/detailed](https://morvo-production.up.railway.app/health/detailed)
