# Top Security Oversights in AI-Generated ("Vibe Coded") Applications

With the rapid emergence of AI app generators (Lovable, Cursor, Bolt.new, v0, Windsurf), founders are launching functional web products within minutes. However, security boundaries that traditional software engineering workflows enforce are frequently missed by AI prompts.

## 1. Supabase Row Level Security (RLS) Omission
- **The Issue**: AI assistants create tables via SQL migrations or dashboard builders without adding explicit `ENABLE ROW LEVEL SECURITY` statements.
- **Consequence**: The anonymous public key (`anon`) has full read/write access to customer database tables via the default PostgREST REST interface.
- **Fix**: Run `ALTER TABLE <table_name> ENABLE ROW LEVEL SECURITY;` on all public tables immediately upon creation.

## 2. Hardcoded API Keys in Client Bundles
- **The Issue**: Developers prompt models with third-party keys (OpenAI, Stripe secret keys, Resend, Twilio), which get committed into `.env` or Vite/Webpack client-side code (`VITE_*`, `NEXT_PUBLIC_*`).
- **Consequence**: Any user inspecting DevTools can capture the secret keys and drain quota or impersonate the service.
- **Fix**: Move secret calls to edge functions or backend server routes. Only public publishable keys belong on the client.

## 3. Wildcard CORS Configuration
- **The Issue**: AI assistants default to `Access-Control-Allow-Origin: *` to avoid frustrating local development CORS errors.
- **Consequence**: Malicious third-party websites visited by users can send cross-origin requests to private endpoints and intercept sensitive responses.
- **Fix**: Restrict allowed origins strictly to the production and staging domains.

## 4. Unprotected Webhook Endpoints
- **The Issue**: AI models implement Stripe or payment webhook receivers without verifying cryptographic signatures (`stripe.webhooks.constructEvent`).
- **Consequence**: Attackers can spoof fake `checkout.session.completed` payloads to unlock premium features without paying.
- **Fix**: Verify incoming webhook HMAC signatures using signing secrets.

## 5. Missing Basic HTTP Security Headers
- **The Issue**: Simple static hosts serve frontend assets without CSP, HSTS, or clickjacking headers.
- **Consequence**: Reduced SEO trust scores, exposure to clickjacking iframes, and vulnerability to third-party script injection.
- **Fix**: Configure automated header injection at the CDN/gateway level.

---
### Audit Your Application
- Instant Free Scanner: [VibeGuard Scanner](https://vibeguard-scanner.surge.sh)
- Automated API Endpoint: `POST https://carey-safari-nicholas-corresponding.trycloudflare.com/api/v1/audit/supabase`
- Custom Security Audit & Fix Package: [Order Audit ($29)](https://newchannelid432-code.github.io/vibeaudit-landing/pay.html)
