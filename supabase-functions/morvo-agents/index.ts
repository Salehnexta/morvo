import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient, SupabaseClient } from 'https://esm.sh/@supabase/supabase-js@2';

// MCP Protocol interfaces
interface MCPResource {
  uri: string;
  type: 'database' | 'schema' | 'analytics';
  data: any;
  timestamp: number;
}

interface A2AMessage {
  from: string;
  to: string;
  endpoint: string;
  payload: any;
  timestamp: number;
}

// Enhanced Morvo Agent with MCP & A2A
class EnhancedMorvoAgent {
  private supabase: any;
  private mcpResources: Map<string, MCPResource> = new Map();
  private a2aQueue: A2AMessage[] = [];

  constructor(supabaseUrl: string, supabaseKey: string) {
    this.supabase = createClient(supabaseUrl, supabaseKey);
  }

  // MCP Protocol Methods
  async registerMCPResource(uri: string, type: MCPResource['type'], data: any): Promise<void> {
    this.mcpResources.set(uri, {
      uri,
      type,
      data,
      timestamp: Date.now()
    });
  }

  async getMCPResource(uri: string): Promise<any> {
    const resource = this.mcpResources.get(uri);
    return resource?.data || null;
  }

  // A2A Protocol Methods
  async sendA2AMessage(from: string, to: string, endpoint: string, payload: any): Promise<string> {
    const message: A2AMessage = {
      from,
      to,
      endpoint,
      payload,
      timestamp: Date.now()
    };
    
    this.a2aQueue.push(message);
    return `message_${Date.now()}`;
  }

  async receiveA2AMessages(agentId: string): Promise<A2AMessage[]> {
    return this.a2aQueue.filter(msg => msg.to === agentId);
  }

  // Initialize MCP resources from Supabase
  async initializeMCPResources(): Promise<void> {
    try {
      // Load user profiles as MCP resource
      const { data: profiles } = await this.supabase
        .from('profiles')
        .select('*')
        .limit(10);
      
      await this.registerMCPResource('data://supabase/profiles', 'database', profiles);

      // Load marketing campaigns as MCP resource
      const { data: campaigns } = await this.supabase
        .from('marketing_campaigns')
        .select('*')
        .limit(10);
      
      await this.registerMCPResource('data://supabase/campaigns', 'database', campaigns);

      // Load analytics data as MCP resource
      const { data: analytics } = await this.supabase
        .from('analytics_access')
        .select('*')
        .limit(10);
      
      await this.registerMCPResource('analytics://data/access', 'analytics', analytics);

    } catch (error) {
      console.error('Error initializing MCP resources:', error);
    }
  }

  // Enhanced KPI calculation with MCP data
  async calculateKPIsWithMCP(userId: string): Promise<any> {
    const profilesData = await this.getMCPResource('data://supabase/profiles');
    const campaignsData = await this.getMCPResource('data://supabase/campaigns');
    const analyticsData = await this.getMCPResource('analytics://data/access');

    return {
      total_orders: campaignsData?.length || 0,
      total_products: profilesData?.length || 0,
      recent_sentiment: analyticsData?.slice(-3) || [],
      mcp_data_sources: ['profiles', 'campaigns', 'analytics'],
      a2a_collaborations: this.a2aQueue.length
    };
  }
}

export default {
  async fetch(request: Request): Promise<Response> {
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
    };

    if (request.method === 'OPTIONS') {
      return new Response('ok', { headers: corsHeaders });
    }

    try {
      const { message, userId, conversationId } = await request.json();

      // Initialize Enhanced Morvo Agent with MCP & A2A
      const supabaseUrl = globalThis.Deno?.env.get('SUPABASE_URL') || '';
      const supabaseKey = globalThis.Deno?.env.get('SUPABASE_ANON_KEY') || '';
      const openaiApiKey = globalThis.Deno?.env.get('OPENAI_API_KEY') || '';

      const morvoAgent = new EnhancedMorvoAgent(supabaseUrl, supabaseKey);
      const supabase = createClient(supabaseUrl, supabaseKey);

      // 1. Initialize MCP resources
      await morvoAgent.initializeMCPResources();

      // 2. Get active system prompt from Supabase
      const { data: systemPrompt } = await supabase
        .from('system_prompts')
        .select('prompt_text')
        .eq('name', 'morvo_main')
        .eq('is_active', true)
        .single();

      // 3. Get conversation context with MCP enhancement
      const { data: conversationHistory } = await supabase
        .from('morvo_conversations')
        .select('*')
        .eq('conversation_id', conversationId)
        .order('created_at', { ascending: true })
        .limit(10);

      // 4. Calculate KPIs with MCP data
      const kpiContext = await morvoAgent.calculateKPIsWithMCP(userId);

      // 5. Enable A2A collaboration
      await morvoAgent.sendA2AMessage(
        'morvo_main',
        'data_analyst',
        'collaboration',
        { user_message: message, context: kpiContext }
      );

      // 6. Build enhanced prompt with MCP context and A2A collaboration
      const mcpContextSummary = {
        profiles_loaded: !!(await morvoAgent.getMCPResource('data://supabase/profiles')),
        campaigns_loaded: !!(await morvoAgent.getMCPResource('data://supabase/campaigns')),
        analytics_loaded: !!(await morvoAgent.getMCPResource('analytics://data/access'))
      };

      const enhancedPrompt = `${systemPrompt?.prompt_text || ''}

CURRENT USER CONTEXT (Enhanced with MCP):
- الطلبات: ${kpiContext.total_orders}
- المنتجات: ${kpiContext.total_products}
- المشاعر الأخيرة: ${JSON.stringify(kpiContext.recent_sentiment)}
- مصادر البيانات MCP: ${kpiContext.mcp_data_sources.join(', ')}
- التعاون A2A النشط: ${kpiContext.a2a_collaborations} رسائل

CONVERSATION HISTORY:
${conversationHistory?.map(msg => `${msg.message_type}: ${msg.content}`).join('\n') || 'لا توجد محادثات سابقة'}

MCP RESOURCES STATUS:
${JSON.stringify(mcpContextSummary, null, 2)}

الآن أجب على رسالة المستخدم بما يتناسب مع سياقه التجاري والبيانات المتاحة عبر MCP:`;

      // 7. Call OpenAI with enhanced context
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${openaiApiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'gpt-4o',
          messages: [
            { role: 'system', content: enhancedPrompt },
            { role: 'user', content: message }
          ],
          max_tokens: 500,
          temperature: 0.7,
        }),
      });

      const aiResponse = await response.json();
      const morvoReply = aiResponse.choices[0]?.message?.content || 'أعتذر، لم أتمكن من معالجة طلبك.';

      // 8. Store conversation with MCP and A2A metadata
      await supabase
        .from('morvo_conversations')
        .insert([
          {
            user_id: userId,
            conversation_id: conversationId,
            message_type: 'user',
            content: message,
            context_data: {
              mcp_resources_used: kpiContext.mcp_data_sources,
              a2a_collaborations: kpiContext.a2a_collaborations,
              kpi_context: kpiContext
            }
          },
          {
            user_id: userId,
            conversation_id: conversationId,
            message_type: 'assistant',
            content: morvoReply,
            context_data: {
              system_prompt_used: 'morvo_main',
              mcp_context: mcpContextSummary,
              a2a_enabled: true
            }
          }
        ]);

      return new Response(
        JSON.stringify({
          reply: morvoReply,
          conversationId,
          metadata: {
            mcp_resources_loaded: Object.keys(mcpContextSummary).filter(k => mcpContextSummary[k]).length,
            a2a_messages: kpiContext.a2a_collaborations,
            data_sources: kpiContext.mcp_data_sources
          }
        }),
        {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 200,
        }
      );

    } catch (error) {
      console.error('Error in Morvo Agent:', error);
      return new Response(
        JSON.stringify({ 
          error: 'خطأ في معالجة الطلب',
          details: error.message,
          mcp_enabled: false,
          a2a_enabled: false
        }),
        {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500,
        }
      );
    }
  },
};
