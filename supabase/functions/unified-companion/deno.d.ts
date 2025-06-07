// Type declarations for Deno modules
declare module "https://deno.land/std@0.182.0/http/server.ts" {
  export function serve(handler: (request: Request) => Response | Promise<Response>): void;
}

declare module "https://esm.sh/@supabase/supabase-js@2.21.0" {
  export interface SupabaseClientOptions {
    auth?: {
      autoRefreshToken?: boolean;
      persistSession?: boolean;
      detectSessionInUrl?: boolean;
    };
    global?: {
      headers?: Record<string, string>;
      fetch?: typeof fetch;
    };
  }

  export interface SupabaseClient {
    from: (table: string) => {
      select: (columns?: string) => {
        eq: (column: string, value: any) => {
          order: (column: string, options?: { ascending?: boolean }) => {
            limit: (count: number) => {
              execute: () => Promise<{ data: any; error: any }>;
            };
            execute: () => Promise<{ data: any; error: any }>;
          };
          eq: (column: string, value: any) => {
            single: () => Promise<{ data: any; error: any }>;
          };
          single: () => Promise<{ data: any; error: any }>;
        };
        order: (column: string, options?: { ascending?: boolean }) => {
          limit: (count: number) => {
            execute: () => Promise<{ data: any; error: any }>;
          };
        };
      };
      insert: (data: any) => {
        select: (columns?: string) => {
          execute: () => Promise<{ data: any; error: any }>;
          single: () => Promise<{ data: any; error: any }>;
        };
        execute: () => Promise<{ data: any; error: any }>;
      };
      update: (data: any) => {
        eq: (column: string, value: any) => {
          execute: () => Promise<{ data: any; error: any }>;
        };
        in: (column: string, values: any[]) => {
          execute: () => Promise<{ data: any; error: any }>;
        };
      };
      delete: () => {
        eq: (column: string, value: any) => {
          execute: () => Promise<{ data: any; error: any }>;
        };
      };
    };
    rpc: (functionName: string, params?: any) => any;
  }

  export function createClient(url: string, key: string, options?: SupabaseClientOptions): SupabaseClient;
}

declare module "https://esm.sh/openai@4.6.0" {
  export interface OpenAIOptions {
    apiKey: string;
    organization?: string;
    baseURL?: string;
    maxRetries?: number;
  }

  export interface ChatCompletionMessage {
    role: "system" | "user" | "assistant" | "function";
    content: string;
    name?: string;
  }

  export interface ChatCompletionOptions {
    model: string;
    messages: ChatCompletionMessage[];
    temperature?: number;
    max_tokens?: number;
    top_p?: number;
    frequency_penalty?: number;
    presence_penalty?: number;
    stream?: boolean;
  }

  export interface ChatCompletionResponse {
    id: string;
    object: string;
    created: number;
    model: string;
    choices: {
      index: number;
      message: ChatCompletionMessage;
      finish_reason: string;
    }[];
    usage: {
      prompt_tokens: number;
      completion_tokens: number;
      total_tokens: number;
    };
  }

  export default class OpenAI {
    constructor(options: OpenAIOptions);
    chat: {
      completions: {
        create: (options: ChatCompletionOptions) => Promise<ChatCompletionResponse>;
      };
    };
  }
}
