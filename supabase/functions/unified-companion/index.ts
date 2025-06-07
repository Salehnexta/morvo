// Morvo AI - Unified Companion Edge Function
// مورفو - الرفيق الموحد للتسويق

// deno-lint-ignore-file no-explicit-any

// Add TypeScript interfaces for Deno global
declare global {
  interface Window {
    Deno: {
      env: {
        get(key: string): string | undefined;
      };
    };
  }
}

// Use var to make Deno available in the global scope for TypeScript
var Deno = window.Deno;

// Deno imports
import { serve } from "https://deno.land/std@0.182.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.21.0";
import OpenAI from "https://esm.sh/openai@4.6.0";

// Types
interface RequestBody {
  message: string;
  user_id: string;
  conversation_id?: string;
  context?: {
    business_type?: string;
    language?: string;
    [key: string]: any;
  };
}

interface SystemPrompt {
  content: string;
}

interface Memory {
  id: string;
  content: any;
  memory_type: string;
  importance: number;
}

// Environment variables - support multiple environment variable names to be flexible
const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
// Support both key naming conventions
const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY") || Deno.env.get("SUPABASE_KEY") || "";
// Support both service role key naming conventions
const supabaseServiceKey = 
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || 
  Deno.env.get("SUPABASE_ACCESS_TOKEN") || 
  "";
const openaiApiKey = Deno.env.get("OPENAI_API_KEY") || "";

// Create clients
const supabaseClient = createClient(supabaseUrl, supabaseServiceKey);
// Create OpenAI client with safety check
const openaiClient = new OpenAI({
  apiKey: openaiApiKey || "missing-key"
});

async function handler(req: Request): Promise<Response> {
  try {
    // Handle CORS preflight
    if (req.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
      });
    }

    // Parse request body
    const requestBody = await req.json() as RequestBody;
    
    if (!requestBody.message || !requestBody.user_id) {
      return new Response(
        JSON.stringify({ error: "Message and user_id are required" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // Create or retrieve conversation
    let conversationId = requestBody.conversation_id;
    if (!conversationId) {
      // Create a new conversation
      const { data: conversation, error } = await supabaseClient
        .from("conversations")
        .insert({
          user_id: requestBody.user_id,
          metadata: {
            business_type: requestBody.context?.business_type || 'unknown',
            language: requestBody.context?.language || 'arabic',
          }
        })
        .select("id")
        .single();
      
      if (error) throw new Error(`Error creating conversation: ${error.message}`);
      conversationId = conversation.id;
    }

    // Store user message
    await supabaseClient
      .from("messages")
      .insert({
        conversation_id: conversationId,
        role: "user",
        content: requestBody.message,
      });

    // Fetch system prompt
    const { data: promptData } = await supabaseClient
      .from("prompts")
      .select("content")
      .eq("name", "morvo_unified_companion")
      .eq("is_active", true)
      .single();

    // Default prompt if none found in database
    // Default Gulf-friendly Arabic system prompt if not found in database
  const systemPrompt = promptData?.content || `أنت «مورفو» – رفيق تسويق ذكي واحد.
    • تحدّث بالعربية الفصحى بلمسة خليجية ودودة.
    • وظيفتك تبسيط التسويق: تحليل SEO، أفكار محتوى، حملات، تتبّع ROI.
    • لا تذكر أي لوحة تحكّم أو جداول معقّدة؛ كل شيء يتمّ داخل المحادثة.
    • جمَل قصيرة، أفعال مباشرة، إيموجي واحد كحدّ أقصى.
    • لا تتجاوز 300 كلمة في أي ردّ.
    • اربط كل أفكارك دائما بنتائج ومؤشرات الأداء الرئيسية للأعمال.
    • اجعل الجمهور المستهدف دائما في قلب استراتيجيتك.
    • قدم دائما معلومات قائمة على البيانات والأدلة عند الإمكان.`;

    // Retrieve user's recent memories
    const { data: memories } = await supabaseClient
      .from("agent_memories")
      .select("id, content, memory_type, importance")
      .eq("user_id", requestBody.user_id)
      .order("importance", { ascending: false })
      .order("updated_at", { ascending: false })
      .limit(5);
    
    // Build context from memories
    let contextFromMemories = "";
    if (memories && memories.length > 0) {
      contextFromMemories = "\nمعلومات سابقة عن المستخدم:\n";
      memories.forEach((memory: Memory) => {
        contextFromMemories += `${memory.memory_type}: ${JSON.stringify(memory.content)}\n`;
      });
    }
    
    // Update last access for memory tracking
    if (memories?.length > 0) {
      const memoryIds = memories.map((m: Memory) => m.id);
      await supabaseClient
        .from("agent_memories")
        .update({ 
          last_accessed_at: new Date().toISOString(),
          access_count: supabaseClient.rpc('increment', { access_count: 1 })
        })
        .in("id", memoryIds);
    }

    // Get conversation history (last 5 messages)
    const { data: messageHistory } = await supabaseClient
      .from("messages")
      .select("role, content")
      .eq("conversation_id", conversationId)
      .order("created_at", { ascending: false })
      .limit(10);
    
    const conversationHistory = messageHistory ? 
      messageHistory.reverse().map((msg: any) => ({
        role: msg.role,
        content: msg.content
      })) : [];

    // Create message for OpenAI
    const messages = [
      { role: "system", content: systemPrompt + contextFromMemories },
      ...conversationHistory,
    ];

    // Call OpenAI API
    const completion = await openaiClient.chat.completions.create({
      model: "gpt-4-turbo-preview",
      messages,
      temperature: 0.7,
      max_tokens: 800,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0.6,
    });

    const responseText = completion.choices[0].message.content || "";

    // Store assistant response
    await supabaseClient
      .from("messages")
      .insert({
        conversation_id: conversationId,
        role: "assistant",
        content: responseText,
      });
    
    // Update conversation last_message_at
    await supabaseClient
      .from("conversations")
      .update({ last_message_at: new Date().toISOString() })
      .eq("id", conversationId);

    // Return response
    return new Response(
      JSON.stringify({
        response: responseText,
        conversation_id: conversationId,
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    );
  } catch (error) {
    console.error("Error:", error.message);
    return new Response(
      JSON.stringify({ error: `Internal server error: ${error.message}` }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}

// Start the Edge Function server
console.log("🚀 Morvo Unified Companion Edge Function Started");
console.log(`Supabase URL configured: ${supabaseUrl ? 'Yes' : 'No'}`);
console.log(`Supabase Keys configured: ${supabaseAnonKey && supabaseServiceKey ? 'Yes' : 'No'}`);
console.log(`OpenAI API Key configured: ${openaiApiKey ? 'Yes' : 'No'}`);

serve(handler);
