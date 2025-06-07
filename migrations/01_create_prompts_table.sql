-- Migration: 01_create_prompts_table.sql
-- Creates the prompts table for storing system prompts for the unified "مورفو" companion

-- Create prompts table
CREATE TABLE IF NOT EXISTS public.prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    category VARCHAR(100),
    version VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Add unique constraint on name for active prompts
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_active_prompts ON public.prompts (name) WHERE is_active = true;

-- Add comment
COMMENT ON TABLE public.prompts IS 'System prompts for Morvo AI agents and the unified companion';

-- Insert default prompt for unified companion
INSERT INTO public.prompts (name, content, is_active, category, version)
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
    'system_prompt',
    '2.0.0'
) ON CONFLICT (name) WHERE is_active = true 
DO UPDATE SET 
    content = EXCLUDED.content,
    updated_at = now(),
    version = EXCLUDED.version;

-- Create Row Level Security policies
ALTER TABLE public.prompts ENABLE ROW LEVEL SECURITY;

-- Policy for viewing prompts - anyone authenticated can view
CREATE POLICY prompts_view_policy ON public.prompts 
    FOR SELECT USING (true);

-- Policy for editing prompts - only admins can edit
CREATE POLICY prompts_edit_policy ON public.prompts 
    FOR UPDATE USING (auth.jwt() ->> 'role' = 'admin');

-- Policy for inserting prompts - only admins can insert
CREATE POLICY prompts_insert_policy ON public.prompts 
    FOR INSERT WITH CHECK (auth.jwt() ->> 'role' = 'admin');

-- Policy for deleting prompts - only admins can delete
CREATE POLICY prompts_delete_policy ON public.prompts 
    FOR DELETE USING (auth.jwt() ->> 'role' = 'admin');
