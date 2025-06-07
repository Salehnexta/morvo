# 🚀 LOVABLE INTEGRATION PROMPTS - Copy & Paste Ready

## ⚡ **STEP 1: Copy this EXACT prompt into Lovable:**

```
Create a Morvo AI dashboard that connects to our backend API. Build the following features:

1. **Agent Status Dashboard**: 
   - Show 5 AI agents (M1-M5) with Arabic names and specializations
   - Real-time status indicators with green/red colors
   - Agent cards with modern design using Tailwind CSS

2. **API Integration Service**:
   - Base URL: https://morvo-production.up.railway.app
   - Health check: GET /health
   - Agent status: GET /api/v2/chat/agents/status
   - Chat endpoint: POST /api/v2/chat/message

3. **Chat Interface**:
   - Select agent dropdown (M1-M5)
   - Message input and send button
   - Chat history display
   - Loading states and error handling

4. **Modern UI**:
   - Dark theme with gradient backgrounds
   - Responsive design for mobile and desktop
   - Beautiful cards and animations
   - Loading spinners and success/error states

Include proper TypeScript types and error handling for all API calls.
```

---

## ⚡ **STEP 2: After Step 1 works, add Supabase:**

```
Connect this app to Supabase for user authentication and data storage:

1. **Add Supabase Auth**:
   - Email/password login and signup
   - User profile management
   - Protected routes for authenticated users

2. **Database Integration**:
   - Store chat conversations in 'conversations' table
   - Track agent usage in 'agent_usage' table
   - User profiles in 'user_profiles' table

3. **Supabase Configuration**:
   - URL: https://teniefzxdikestahndur.supabase.co
   - Use the anon key from environment variables

4. **Enhanced Features**:
   - Chat history per user
   - Usage analytics dashboard
   - User settings page

Make sure to handle authentication state and redirect users properly.
```

---

## ⚡ **STEP 3: Add Advanced Features:**

```
Add these advanced Morvo AI features:

1. **SEO Audit Tool**:
   - Website URL input form
   - Call API: POST /api/v2/seo/audit with {"website": "url", "detailed": false}
   - Display audit results in a beautiful dashboard
   - Save audit history to Supabase

2. **Analytics Dashboard**:
   - Show API status: GET /api/v2/analytics/providers/status
   - Display provider costs and activation dates
   - Usage charts and statistics

3. **Agent Specialization Pages**:
   - Dedicated page for each agent (M1-M5)
   - Show agent capabilities and examples
   - Specialized chat interfaces per agent

4. **Real-time Features**:
   - WebSocket connection for live updates
   - Real-time agent status monitoring
   - Live chat notifications

Include beautiful charts, graphs, and data visualizations.
```

---

## ⚡ **STEP 4: Production Deployment:**

```
Prepare the app for production deployment to morvo.ai:

1. **Performance Optimization**:
   - Add loading states for all API calls
   - Implement caching for agent status
   - Optimize images and assets

2. **SEO and Meta Tags**:
   - Add proper meta tags for morvo.ai
   - Open Graph tags for social sharing
   - Sitemap and robots.txt

3. **Error Handling**:
   - Global error boundary
   - API timeout handling
   - User-friendly error messages

4. **Security**:
   - API key management
   - Rate limiting consideration
   - Input validation and sanitization

5. **Mobile Optimization**:
   - Touch-friendly interface
   - Mobile-first responsive design
   - PWA features if possible

Make it production-ready for launch on morvo.ai domain.
```

---

## 🗂️ **Files to Upload to Supabase:**

1. **Run this SQL in Supabase SQL Editor:**
   ```sql
   -- Copy content from supabase-schema.sql file
   ```

2. **Create Edge Function:**
   ```typescript
   -- Copy content from supabase-functions/morvo-agents/index.ts
   ```

---

## 🎯 **Environment Variables for Lovable:**

```env
NEXT_PUBLIC_MORVO_API_URL=https://morvo-production.up.railway.app
NEXT_PUBLIC_SUPABASE_URL=https://teniefzxdikestahndur.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlbmllZnp4ZGlrZXN0YWhkbnVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg2MjI2NTIsImV4cCI6MjA2NDE5ODY1Mn0.k5eor_-j2aTheb1q6OhGK8DWGjucRWK11eFAOpAZP3I
```

---

## ✅ **Testing URLs:**

- **Health**: https://morvo-production.up.railway.app/health
- **Agents**: https://morvo-production.up.railway.app/api/v2/chat/agents/status
- **Analytics**: https://morvo-production.up.railway.app/api/v2/analytics/providers/status

---

## 🚀 **Instructions:**

1. **Copy Step 1 prompt** → Paste in Lovable chat → Wait for completion
2. **Test the basic dashboard** → Verify API connections work
3. **Copy Step 2 prompt** → Add Supabase integration
4. **Copy Step 3 prompt** → Add advanced features
5. **Copy Step 4 prompt** → Prepare for production

**Each step builds on the previous one. Don't skip steps!**
