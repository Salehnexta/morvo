-- Unified Morvo Companion Database Schema
-- Combines prompts table and MCP tables for simplified deployment

-- Create prompts table for system prompt storage
CREATE TABLE IF NOT EXISTS public.prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Add unique constraint for active prompts with the same name
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_active_prompts ON public.prompts (name) WHERE is_active = true;

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_prompts_name ON public.prompts (name);
CREATE INDEX IF NOT EXISTS idx_prompts_is_active ON public.prompts (is_active);

-- Add comment
COMMENT ON TABLE public.prompts IS 'System prompts for Morvo AI agents';

-- Enable Row Level Security
ALTER TABLE public.prompts ENABLE ROW LEVEL SECURITY;

-- Create policies to control access to prompts
-- Allow all users to read prompts
CREATE POLICY prompts_read_policy ON public.prompts 
    FOR SELECT USING (true);

-- Only allow admin to insert/update/delete prompts
CREATE POLICY prompts_write_policy ON public.prompts 
    FOR ALL USING (auth.jwt() ? 'admin_access');

-- Insert default unified companion system prompt (Gulf-friendly Arabic)
INSERT INTO public.prompts (name, content, is_active, version)
VALUES (
    'morvo_unified_companion',
    'أنت «مورفو» – رفيق تسويق ذكي واحد.
• تحدّث بالعربية الفصحى بلمسة خليجية ودودة.
• وظيفتك تبسيط التسويق: تحليل SEO، أفكار محتوى، حملات، تتبّع ROI.
• لا تذكر أي لوحة تحكّم أو جداول معقّدة؛ كل شيء يتمّ داخل المحادثة.
• جمَل قصيرة، أفعال مباشرة، إيموجي واحد كحدّ أقصى.
• لا تتجاوز 300 كلمة في أي ردّ.
• اربط كل أفكارك دائما بنتائج ومؤشرات الأداء الرئيسية للأعمال.
• اجعل الجمهور المستهدف دائما في قلب استراتيجيتك.
• قدم دائما معلومات قائمة على البيانات والأدلة عند الإمكان.',
    true,
    1
) ON CONFLICT (name) WHERE is_active = true
DO UPDATE SET 
    content = EXCLUDED.content,
    version = public.prompts.version + 1,
    updated_at = now();

-- Create agent_memories table for MCP protocol
CREATE TABLE IF NOT EXISTS public.agent_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(50) NOT NULL,
    user_id UUID NOT NULL,
    memory_type VARCHAR(50) NOT NULL,
    content JSONB NOT NULL,
    importance INTEGER DEFAULT 5,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    last_accessed_at TIMESTAMPTZ,
    access_count INTEGER DEFAULT 0
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_agent_memories_agent_id ON public.agent_memories (agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_memories_user_id ON public.agent_memories (user_id);
CREATE INDEX IF NOT EXISTS idx_agent_memories_memory_type ON public.agent_memories (memory_type);
CREATE INDEX IF NOT EXISTS idx_agent_memories_importance ON public.agent_memories (importance DESC);

-- Add comment
COMMENT ON TABLE public.agent_memories IS 'Agent memories for MCP protocol implementation, supporting unified مورفو companion';

-- Create cross_agent_context table for enhanced A2A protocol
CREATE TABLE IF NOT EXISTS public.cross_agent_context (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    context_key VARCHAR(255) NOT NULL,
    context_data JSONB NOT NULL,
    context_type VARCHAR(50) NOT NULL,
    source_agent_id VARCHAR(50),
    shared_with JSONB, -- Array of agent IDs that have access
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Add unique constraint on context_key
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_context_key ON public.cross_agent_context (context_key);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_cross_agent_context_type ON public.cross_agent_context (context_type);
CREATE INDEX IF NOT EXISTS idx_cross_agent_context_source ON public.cross_agent_context (source_agent_id);

-- Add comment
COMMENT ON TABLE public.cross_agent_context IS 'Cross-agent shared context for A2A protocol integration';

-- Create conversations table to track user interactions with the unified companion
CREATE TABLE IF NOT EXISTS public.conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    companion_name VARCHAR(255) DEFAULT 'مورفو',
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    last_message_at TIMESTAMPTZ DEFAULT now()
);

-- Create messages table for conversation history
CREATE TABLE IF NOT EXISTS public.messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON public.messages (conversation_id);
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON public.conversations (user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_last_message ON public.conversations (last_message_at DESC);

-- Set up RLS policies for these tables
ALTER TABLE public.agent_memories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cross_agent_context ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

-- RLS policies for agent_memories - access by user_id
CREATE POLICY agent_memories_user_policy ON public.agent_memories 
    FOR ALL USING (auth.uid() = user_id);

-- RLS policies for cross_agent_context - available to all authenticated users
CREATE POLICY cross_agent_context_policy ON public.cross_agent_context 
    FOR SELECT USING (true);

-- RLS policies for conversations - access by user_id
CREATE POLICY conversations_user_policy ON public.conversations 
    FOR ALL USING (auth.uid() = user_id);

-- RLS policies for messages - access through conversation ownership
CREATE POLICY messages_conversation_policy ON public.messages 
    FOR ALL USING (
        conversation_id IN (
            SELECT id FROM public.conversations WHERE user_id = auth.uid()
        )
    );
