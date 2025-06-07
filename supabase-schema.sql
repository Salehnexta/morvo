-- Morvo AI - Supabase Database Schema
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  subscription_plan TEXT DEFAULT 'free',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  agent_id TEXT NOT NULL,
  message TEXT NOT NULL,
  response JSONB,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- SEO audits table
CREATE TABLE IF NOT EXISTS seo_audits (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  website TEXT NOT NULL,
  results JSONB NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent usage tracking
CREATE TABLE IF NOT EXISTS agent_usage (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  agent_id TEXT NOT NULL,
  action TEXT NOT NULL,
  usage_count INTEGER DEFAULT 1,
  date DATE DEFAULT CURRENT_DATE,
  UNIQUE(user_id, agent_id, action, date)
);

-- Campaign data table (for future use)
CREATE TABLE IF NOT EXISTS campaigns (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  target_audience JSONB,
  budget_amount DECIMAL,
  start_date DATE,
  end_date DATE,
  status TEXT DEFAULT 'draft',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System prompts table for Morvo companion
CREATE TABLE IF NOT EXISTS system_prompts (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  prompt_text TEXT NOT NULL,
  version INTEGER DEFAULT 1,
  is_active BOOLEAN DEFAULT true,
  industry_tone TEXT DEFAULT 'general',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert the main Morvo system prompt
INSERT INTO system_prompts (name, prompt_text, industry_tone) VALUES 
('morvo_main', 'أنت «مورفو» – رفيق تسويق ذكي واحد (وليس مجموعة وكلاء)...', 'gulf_friendly');

-- Unified marketing conversations (replaces old multi-agent approach)
CREATE TABLE IF NOT EXISTS morvo_conversations (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  conversation_id TEXT NOT NULL, -- Session identifier
  message_type TEXT NOT NULL, -- 'user' or 'assistant'
  content TEXT NOT NULL,
  context_data JSONB, -- KPIs, retrieved docs, etc.
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Marketing intelligence cache (for pgvector data)
CREATE TABLE IF NOT EXISTS marketing_intelligence (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  document_type TEXT NOT NULL, -- 'we_are_social', 'google_mena', 'techx_ecommerce'
  industry TEXT,
  region TEXT DEFAULT 'mena',
  content_summary TEXT,
  key_metrics JSONB,
  embedding vector(1536), -- For similarity search
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Unified customer data (consolidates products, orders, sentiment)
CREATE TABLE IF NOT EXISTS unified_customer_data (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  data_type TEXT NOT NULL, -- 'product', 'order', 'sentiment', 'website'
  source_platform TEXT, -- 'shopify', 'woocommerce', 'custom'
  data_payload JSONB NOT NULL,
  kpi_metrics JSONB, -- Pre-calculated KPIs for quick access
  last_synced TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversation context tracking
CREATE TABLE IF NOT EXISTS conversation_context (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  conversation_id TEXT NOT NULL,
  context_type TEXT NOT NULL, -- 'user_profile', 'business_data', 'current_campaign'
  context_data JSONB NOT NULL,
  expires_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security (RLS) Policies
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE seo_audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_prompts ENABLE ROW LEVEL SECURITY;
ALTER TABLE morvo_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_intelligence ENABLE ROW LEVEL SECURITY;
ALTER TABLE unified_customer_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_context ENABLE ROW LEVEL SECURITY;

-- Policies for user_profiles
CREATE POLICY "Users can view own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = id);

-- Policies for conversations
CREATE POLICY "Users can view own conversations" ON conversations
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own conversations" ON conversations
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for seo_audits
CREATE POLICY "Users can view own SEO audits" ON seo_audits
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own SEO audits" ON seo_audits
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for agent_usage
CREATE POLICY "Users can view own usage" ON agent_usage
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own usage" ON agent_usage
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for campaigns
CREATE POLICY "Users can manage own campaigns" ON campaigns
  FOR ALL USING (auth.uid() = user_id);

-- Policies for system_prompts
CREATE POLICY "Users can view system prompts" ON system_prompts
  FOR SELECT USING (true);

-- Policies for morvo_conversations
CREATE POLICY "Users can view own morvo conversations" ON morvo_conversations
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own morvo conversations" ON morvo_conversations
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for marketing_intelligence
CREATE POLICY "Users can view marketing intelligence" ON marketing_intelligence
  FOR SELECT USING (true);

-- Policies for unified_customer_data
CREATE POLICY "Users can view own unified customer data" ON unified_customer_data
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own unified customer data" ON unified_customer_data
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for conversation_context
CREATE POLICY "Users can view own conversation context" ON conversation_context
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own conversation context" ON conversation_context
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Function to handle user profile creation
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.user_profiles (id, email, full_name)
  VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create profile on signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Update timestamp function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaigns_updated_at
    BEFORE UPDATE ON campaigns
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_prompts_updated_at
    BEFORE UPDATE ON system_prompts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_unified_customer_data_updated_at
    BEFORE UPDATE ON unified_customer_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
