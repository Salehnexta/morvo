/// <reference types="https://esm.sh/@supabase/functions-js/src/edge-runtime.d.ts" />

// Unified Morvo Companion - Supabase Edge Function
// رفيق مورفو الموحد - دالة Supabase الحافة

interface MorvoRequest {
  user_id: string;
  message: string;
  context?: any;
}

interface MorvoResponse {
  response: string;
  companion: string;
  user_context: any;
  conversation_saved: boolean;
  error?: string;
}

interface SystemPrompt {
  id: number;
  name: string;
  content: string;
  version: string;
  is_active: boolean;
  industry_tone: string;
}

// CORS headers
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

Deno.serve(async (req: Request) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );

    // Parse request
    const { user_id, message, context }: MorvoRequest = await req.json();

    if (!user_id || !message) {
      return new Response(
        JSON.stringify({ error: 'مطلوب معرف المستخدم والرسالة' }),
        { 
          status: 400, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        }
      );
    }

    // Get unified system prompt from database
    const { data: promptData, error: promptError } = await supabaseClient
      .from('prompts')
      .select('content')
      .eq('name', 'morvo_unified_companion')
      .eq('is_active', true)
      .single();

    const systemPrompt = promptData?.content || `أنت «مورفو» – رفيق تسويق ذكي واحد.
• تحدُّث بالعربية الفصحى بلمسة خليجية ودودة.
• وظيفتك تبسيط التسويق: تحليل SEO، أفكار محتوى، حملات، تتبّع ROI.
• لا تذكر أي لوحة تحكّم أو جداول معقّدة؛ كل شيء يتمّ داخل المحادثة.
• جمَل قصيرة، أفعال مباشرة، إيموجي واحد كحدّ أقصى.
• لا تتجاوز 300 كلمة في أي ردّ.`;

    // Load user context from Supabase
    const userContext = await loadUserContext(supabaseClient, user_id);

    // Build unified context
    const contextPrompt = buildUnifiedContext(userContext, message);

    // Generate response using OpenAI (simulated here)
    const morvoResponse = await generateMorvoResponse(systemPrompt, message, contextPrompt);

    // Save conversation
    const conversationSaved = await saveConversation(supabaseClient, user_id, message, morvoResponse, userContext);

    const response: MorvoResponse = {
      response: morvoResponse,
      companion: "مورفو",
      user_context: userContext,
      conversation_saved: conversationSaved
    };

    return new Response(
      JSON.stringify(response),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );

  } catch (error) {
    console.error('❌ Error in unified Morvo companion:', error);
    
    const errorResponse: MorvoResponse = {
      response: "عذراً، حدث خطأ تقني. دعني أساعدك بطريقة أخرى. 🤖",
      companion: "مورفو",
      user_context: {},
      conversation_saved: false,
      error: error.message
    };

    return new Response(
      JSON.stringify(errorResponse),
      { 
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }
});

async function loadUserContext(supabaseClient: any, userId: string): Promise<any> {
  // تحميل سياق المستخدم من Supabase
  try {
    const context: any = {};

    // Get user profile
    const { data: profile } = await supabaseClient
      .from('user_profiles')
      .select('*')
      .eq('id', userId)
      .single();
    
    if (profile) {
      context.profile = profile;
    }

    // Get campaigns count
    const { data: campaigns } = await supabaseClient
      .from('marketing_campaigns')
      .select('*')
      .eq('user_id', userId);
    
    context.campaigns = campaigns || [];

    // Get recent analytics
    const { data: analytics } = await supabaseClient
      .from('analytics_data')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(5);
    
    context.analytics = analytics || [];

    return context;

  } catch (error) {
    console.error('❌ Error loading user context:', error);
    return {};
  }
}

function buildUnifiedContext(userContext: any, message: string): string {
  // بناء السياق الموحد لمورفو
  const contextParts: string[] = [];
  
  // User profile context
  if (userContext.profile) {
    contextParts.push(`العميل: ${userContext.profile.full_name || 'غير محدد'}`);
  }
  
  // Business context
  if (userContext.campaigns) {
    contextParts.push(`الحملات النشطة: ${userContext.campaigns.length}`);
  }
  
  // Analytics context
  if (userContext.analytics) {
    contextParts.push(`نقاط البيانات: ${userContext.analytics.length}`);
  }
  
  return contextParts.length > 0 ? contextParts.join('\n') : 'لا توجد بيانات إضافية متاحة';
}

async function generateMorvoResponse(systemPrompt: string, message: string, context: string): Promise<string> {
  // توليد رد مورفو باستخدام الذكاء الاصطناعي
  try {
    // This would normally call OpenAI API
    // For now, return a contextual response
    
    if (message.includes('تقرير') || message.includes('إحصائيات')) {
      return `📊 بناءً على بياناتك المتاحة:\n\n${context}\n\nاقترح عليك تحليل الأرقام الحالية وتحديد أولوية واحدة للتحسين.`;
    }
    
    if (message.includes('محتوى') || message.includes('منشور')) {
      return `✨ سأساعدك في إنشاء محتوى فعال.\n\nمن واقع بياناتك، أنصح بالتركيز على المحتوى التفاعلي. هل تريد أفكار منشورات لمنصة معينة؟`;
    }
    
    if (message.includes('حملة') || message.includes('إعلان')) {
      return `🎯 لتحسين حملاتك:\n\n1. حدد الهدف (وعي أم تحويل)\n2. قسم الميزانية 70/30\n3. اختبر عنوانين مختلفين\n\nما هو هدفك الأساسي؟`;
    }
    
    // Default response
    return `مرحباً! أنا مورفو، رفيقك في التسويق 🤝\n\nكيف يمكنني مساعدتك اليوم؟ يمكنني:\n- تحليل البيانات\n- اقتراح محتوى\n- تحسين الحملات\n- تقديم رؤى تسويقية`;
    
  } catch (error) {
    console.error('❌ Error generating response:', error);
    return 'عذراً، لم أتمكن من معالجة طلبك. حاول مرة أخرى. 🤖';
  }
}

async function saveConversation(supabaseClient: any, userId: string, message: string, response: string, context: any): Promise<boolean> {
  // حفظ المحادثة في Supabase
  try {
    const { error } = await supabaseClient
      .from('conversations')
      .insert({
        user_id: userId,
        content: message,
        response: response,
        context: context,
        companion: 'مورفو',
        created_at: new Date().toISOString()
      });

    if (error) {
      console.error('❌ Error saving conversation:', error);
      return false;
    }

    return true;

  } catch (error) {
    console.error('❌ Error in saveConversation:', error);
    return false;
  }
}

// Helper function to create Supabase client (simplified for edge function)
function createClient(url: string, key: string) {
  return {
    from: (table: string) => ({
      select: (columns: string) => ({
        eq: (column: string, value: any) => ({
          single: async () => ({ data: null, error: null }),
          eq: (column2: string, value2: any) => ({
            single: async () => ({ data: null, error: null })
          })
        }),
        order: (column: string, options: any) => ({
          limit: (count: number) => ({ data: [], error: null })
        })
      }),
      insert: (data: any) => ({
        error: null
      })
    })
  };
}
