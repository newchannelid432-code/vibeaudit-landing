# HTTP Security Headers Benchmark & Best Practices (2026)

HTTP security headers provide a critical layer of defense-in-depth against Cross-Site Scripting (XSS), Clickjacking, MIME-type sniffing, and protocol downgrade attacks.

## Critical Headers Overview

| Header | Minimum Recommended Value | Protected Threat |
| :--- | :--- | :--- |
| **Content-Security-Policy** | `default-src 'self'; script-src 'self'; object-src 'none'` | Cross-Site Scripting (XSS), Data Injection |
| **Strict-Transport-Security** | `max-age=31536000; includeSubDomains; preload` | SSL Stripping, MITM Downgrade Attacks |
| **X-Frame-Options** | `DENY` or `SAMEORIGIN` | Clickjacking, Unauthorized Iframe Embedding |
| **X-Content-Type-Options** | `nosniff` | MIME Sniffing, Drive-by Downloads |
| **Access-Control-Allow-Origin** | Whitelisted Origin (Never `*` for Auth APIs) | Unauthorized Cross-Origin Credential Leaks |

## Automated Header Audit API

Query the live VibeSec auditor to verify any web application:

```bash
curl -X POST https://carey-safari-nicholas-corresponding.trycloudflare.com/api/v1/audit/headers \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Sample audit result:
```json
{
  "target": "https://example.com",
  "score": 90,
  "grade": "A",
  "checks": {
    "content_security_policy": {"status": "PASS"},
    "strict_transport_security": {"status": "PASS"},
    "x_frame_options": {"status": "PASS"},
    "x_content_type_options": {"status": "PASS"},
    "cors_policy": {"status": "PASS"}
  }
}
```

## Framework Implementation

### Next.js (`next.config.js`)
```javascript
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
];

module.exports = {
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  },
};
```

### Cloudflare Pages / Workers (`_headers`)
```http
/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';
```

---
*Run an instant header check with [VibeGuard Web Scanner](https://vibeguard-scanner.surge.sh) or consult with our security engineers at [VibeAudit Security](https://newchannelid432-code.github.io/vibeaudit-landing/pay.html).*
