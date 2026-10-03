# Complete Supabase RLS Security & Credential Audit Guide

Modern AI coding platforms like Lovable, Bolt.new, v0, and Cursor frequently scaffold frontend applications connected directly to Supabase databases. While using the `anon` public key on client apps is expected, serious security vulnerabilities occur when developers forget to enable **Row Level Security (RLS)** on backend PostgreSQL tables.

## The Core Risk: Anonymous Data Exfiltration

When a web application embeds:
```javascript
const supabase = createClient(
  'https://xyzcompany.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
)
```
Any visitor or automated scraper can extract this public anon key from the JavaScript bundle. If any database table lacks an active RLS policy, the anon role possesses unrestricted `SELECT`, `INSERT`, `UPDATE`, and `DELETE` permissions via the Supabase PostgREST API:

```bash
# Automated exfiltration test
curl 'https://xyzcompany.supabase.co/rest/v1/users?select=*' \
  -H "apikey: <ANON_KEY>" \
  -H "Authorization: Bearer <ANON_KEY>"
```
If RLS is disabled, this request dumps all private customer records, email addresses, and metadata without requiring user login.

## Detection Methodology

1. **DOM & Script Inspection**: Search HTML documents and loaded script tags for regex pattern `https://[a-z0-9]{20}\.supabase\.co`.
2. **JWT Anon Key Extraction**: Identify JSON Web Tokens with `role: "anon"` in client chunks.
3. **Table Permission Probe**: Query standard schema endpoints to verify whether default `DENY` policies are enforced.

## Automated Verification API

Developers and security teams can run instant programmatic checks using the VibeSec API:

```bash
curl -X POST https://carey-safari-nicholas-corresponding.trycloudflare.com/api/v1/audit/supabase \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-app-domain.com"}'
```

Response format:
```json
{
  "target": "https://your-app-domain.com",
  "supabase_detected": true,
  "project_refs_found": 1,
  "anonymized_refs": ["xyzc***any"],
  "anon_jwt_detected": true,
  "security_recommendation": "Ensure all Postgres tables have 'ALTER TABLE <name> ENABLE ROW LEVEL SECURITY;' applied."
}
```

## Remediation Checklist

1. **Enable Row Level Security on Every Table**:
   ```sql
   ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
   ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
   ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
   ```
2. **Create Least-Privilege Policies**:
   ```sql
   -- Allow users to view only their own records
   CREATE POLICY "Users can view own data" 
   ON public.profiles 
   FOR SELECT 
   USING (auth.uid() = user_id);
   ```
3. **Protect Service Role Keys**:
   Never include `service_role` secrets in frontend environment files or build outputs.

---
*For a complete automated audit of your web application, scan your domain with [VibeGuard Scanner](https://vibeguard-scanner.surge.sh) or order an expert audit report at [VibeAudit Security](https://newchannelid432-code.github.io/vibeaudit-landing/pay.html).*
