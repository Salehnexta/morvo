-- Migration for unified Morvo companion
-- Date: 2024-06-07

-- 1. Ensure prompts table exists with correct structure
CREATE TABLE IF NOT EXISTS prompts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    content TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    industry_tone TEXT DEFAULT 'gulf_friendly',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Insert/Update the unified companion prompt
INSERT INTO prompts (name, content, version, is_active, industry_tone)
VALUES (
    'morvo_unified_companion',
    'أنت «مورفو» – رفيق تسويق ذكي واحد (وليس مجموعة وكلاء).\n• تحدُّث بالعربية الفصحى بلمسة خليجية ودودة.\n• وظيفتك تبسيط التسويق: تحليل SEO، أفكار محتوى، حملات، تتبّع ROI.\n• لا تذكر أي لوحة تحكّم أو جداول معقّدة؛ كل شيء يتمّ داخل المحادثة.\n• جمَل قصيرة، أفعال مباشرة، إيموجي واحد كحدّ أقصى.\n• لا تتجاوز 300 كلمة في أي ردّ.\n• ركّز على ربط كل شيء بأهداف العمل وقياس الأداء.',
    2,
    true,
    'gulf_friendly'
)
ON CONFLICT (name) 
DO UPDATE SET 
    content = EXCLUDED.content,
    version = EXCLUDED.version,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- 3. Update conversations table to support unified companion
ALTER TABLE conversations 
ADD COLUMN IF NOT EXISTS is_unified BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS context_data JSONB;

-- 4. Create index for better performance
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);

-- 5. Deprecate old agent-specific tables (keep for backward compatibility)
COMMENT ON TABLE agent_usage IS 'DEPRECATED: Agent usage tracking (legacy multi-agent system)';
COMMENT ON COLUMN conversations.agent_id IS 'DEPRECATED: Use unified companion instead';

-- 6. Create function to get active system prompt
CREATE OR REPLACE FUNCTION get_active_prompt(prompt_name TEXT)
RETURNS TEXT AS $$
DECLARE
    prompt_text TEXT;
BEGIN
    SELECT content INTO prompt_text 
    FROM prompts 
    WHERE name = prompt_name 
    AND is_active = true 
    ORDER BY version DESC 
    LIMIT 1;
    
    RETURN COALESCE(prompt_text, 'Default system prompt not found');
END;
$$ LANGUAGE plpgsql;

-- 7. Update RLS policies if needed
ALTER TABLE prompts ENABLE ROW LEVEL SECURITY;

-- 8. Create policy to allow public read access to active prompts
CREATE POLICY "Allow public read access to active prompts" 
ON prompts FOR SELECT 
USING (is_active = true);
