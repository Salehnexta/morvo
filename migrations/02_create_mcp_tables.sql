-- Migration: 02_create_mcp_tables.sql
-- Creates the agent_memories and cross_agent_context tables for MCP protocol implementation

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
