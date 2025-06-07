# مورفو (Morvo) - Unified Marketing Companion Edge Function

This Edge Function implements the unified "مورفو" companion API for the Morvo AI platform.

## Features

- **Unified Conversational Experience**: Single companion integrating all marketing expertise
- **Gulf-friendly Arabic Responses**: Culturally appropriate tone with business focus
- **System Prompt from Database**: Dynamically loads system prompt from Supabase
- **MCP Integration**: Accesses user memories and context via Model Context Protocol
- **Conversation Management**: Tracks and persists conversation history
- **Secure Authentication**: Uses Supabase service role key for database operations

## Deployment Instructions

1. **Set Environment Variables**:
   ```bash
   supabase secrets set --env-file ./supabase/.env.production
   ```

2. **Deploy the Function**:
   ```bash
   supabase functions deploy unified-companion --project-ref teniefzxdikestahndur
   ```

3. **Test the Function**:
   ```bash
   curl -X POST "https://teniefzxdikestahndur.supabase.co/functions/v1/unified-companion" \
     -H "Content-Type: application/json" \
     -d '{"message": "مرحبًا مورفو", "user_id": "test-user-1"}'
   ```

## Sample Response

```json
{
  "response": "أهلاً بك! 👋 أنا مورفو، رفيقك التسويقي. كيف يمكنني مساعدتك اليوم؟ هل تحتاج إلى تحليل لأداء SEO أو أفكار محتوى جديدة أو استراتيجية حملات؟",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Schema Requirements

Ensure the following tables exist in your Supabase database:
- `prompts`: Stores system prompts
- `conversations`: Tracks user conversations
- `messages`: Stores message history
- `agent_memories`: Stores user-specific context (MCP)
- `cross_agent_context`: Facilitates agent coordination (A2A)

Refer to the migration scripts (`migrations/*.sql`) for the complete schema definition.
