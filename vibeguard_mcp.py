#!/usr/bin/env python3
"""
VibeGuard MCP (Model Context Protocol) Server
Exposes VibeGuard AI App Security Scanning & PostgreSQL RLS Remediation as an MCP tool.
Compatible with Alexa+, Agent Skills, Claude, Cursor, and any MCP-enabled assistant.

Transport: stdio (JSON-RPC 2.0)
API Backend: https://vibeguard-api.vibeguard-scanner.workers.dev
"""

import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://vibeguard-api.vibeguard-scanner.workers.dev"

TOOLS = [
    {
        "name": "scan_app_security",
        "description": "Audits a live AI-generated web application (Lovable, Bolt, v0, Replit) for unauthenticated Supabase database exposures and missing Row-Level Security (RLS).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "The target domain or URL to audit (e.g., 'cintila.lovable.app', 'https://myapp.lovable.app')"
                }
            },
            "required": ["target"]
        }
    },
    {
        "name": "generate_rls_patch",
        "description": "Generates copy-pasteable PostgreSQL Row-Level Security (RLS) policies to secure exposed tables identified in a scan.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "The domain name of the app."
                },
                "tables": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of table names to secure (e.g. ['orders', 'profiles', 'leads'])"
                }
            },
            "required": ["target", "tables"]
        }
    }
]

def scan_target(target):
    """Call VibeGuard 24/7 Cloud API to scan target domain."""
    url = f"{API_BASE}/api/scan"
    payload = json.dumps({"target": target}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"error": f"HTTP error {e.code}"}
    except Exception as e:
        return {"error": str(e)}

def generate_rls(target, tables):
    """Generate PostgreSQL RLS statements for specified tables."""
    policies = []
    for t in tables:
        policy = f"""-- Secure public.{t}
ALTER TABLE public.{t} ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.{t} FROM anon;
GRANT ALL ON public.{t} TO authenticated;
CREATE POLICY "Users can only read own {t}" ON public.{t} FOR SELECT TO authenticated USING (auth.uid() = id);"""
        policies.append(policy)
    return "\n\n".join(policies)

def handle_rpc(request):
    """Process incoming JSON-RPC 2.0 request."""
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "vibeguard-mcp",
                    "version": "2.0.0"
                }
            }
        }
    elif method == "notifications/initialized":
        return None
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "scan_app_security":
            target = args.get("target", "")
            result = scan_target(target)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
        elif name == "generate_rls_patch":
            target = args.get("target", "")
            tables = args.get("tables", [])
            sql = generate_rls(target, tables)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": sql
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool not found: {name}"}
            }
    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    else:
        if req_id is not None:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
        return None

def main():
    # CLI standalone mode
    if len(sys.argv) > 1 and sys.argv[1] == "--scan":
        target = sys.argv[2] if len(sys.argv) > 2 else "cintila.lovable.app"
        print(f"[*] Scanning {target} via VibeGuard Cloud API...")
        res = scan_target(target)
        print(json.dumps(res, indent=2))
        sys.exit(0)

    # stdio JSON-RPC loop
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            if resp:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
