# VibeGuard: Model Context Protocol (MCP) Server

VibeGuard is an autonomous security scanner and PostgreSQL Row-Level Security (RLS) remediation engine designed for AI-generated applications (Lovable, Bolt, v0, Replit).

This repository contains the **VibeGuard MCP Server**, enabling **Alexa+**, **Bee (Wearable AI)**, and agentic AI coding assistants to audit deployments and generate RLS patches through standard Model Context Protocol tool calling.

---

## 🚀 Key Features

* **Open MCP Standard:** Compliant with Model Context Protocol specification (`protocolVersion: 2024-11-05`) over `stdio` and Streamable HTTP.
* **Agentic Security Audits:** Allows **Alexa+**, **Bee (Wearable AI)**, or autonomous coding agents to inspect public PostgREST tables for unauthenticated exposure.
* **NVIDIA Nemotron Policy Synthesis:** Integrates **NVIDIA Nemotron** (`nvidia/nemotron-4-340b-instruct`) via **Nebius Token Factory** to synthesize context-aware, production-ready PostgreSQL Row-Level Security (RLS) policies.
* **Instant RLS Remediation:** Locks down leaked tables while preserving authentic application functionality, with deterministic rule fallback when offline.
* **Zero Overhead:** Python standard library only. No heavy frameworks or external dependencies required.

---

## 🛠️ MCP Tools

### 1. `scan_app_security`
Audits a target domain for unauthenticated Supabase database exposures and missing Row-Level Security.
* **Parameters:**
  * `target` (string, required): Domain or URL to scan (e.g., `cintila.lovable.app`).
* **Returns:**
  * Status (`vulnerable` or `clean`), Supabase reference, credential type, exposed table list, and remediation guidance.

### 2. `generate_rls_patch`
Generates copy-pasteable PostgreSQL Row-Level Security policies to lock down exposed tables.
* **Parameters:**
  * `target` (string, required): Domain name.
  * `tables` (array of strings, required): List of tables to protect (e.g. `["orders", "profiles", "leads"]`).
* **Returns:**
  * Executable SQL patch applying `ALTER TABLE ... ENABLE ROW LEVEL SECURITY; REVOKE ALL FROM anon;`.

---

## 📦 Quickstart

### 1. Standalone CLI Audit
```bash
python3 vibeguard_mcp.py --scan cintila.lovable.app
```

### 2. Configure with MCP Clients (Claude Desktop / Cursor / Alexa+ Agent / Nebius Sandbox)
Add VibeGuard to your MCP client configuration (`mcpServers`):

```json
{
  "mcpServers": {
    "vibeguard": {
      "command": "python3",
      "args": ["/path/to/vibeguard_mcp.py"],
      "env": {
        "NEBIUS_API_KEY": "your-nebius-token-factory-key",
        "NEBIUS_MODEL": "nvidia/nemotron-4-340b-instruct"
      }
    }
  }
}
```
*(Note: If `NEBIUS_API_KEY` is omitted, VibeGuard seamlessly uses built-in PostgreSQL rule templates).*

### 3. Example Agent Query
> *"Alexa, scan my deployment at demo-crm.lovable.app and generate the RLS security policy."*

---

## 🌐 Live Web Application & Documentation
* **Web Interface:** [https://vibeguard-scanner.surge.sh](https://vibeguard-scanner.surge.sh)
* **24/7 Cloud API:** `https://vibeguard-api.vibeguard-scanner.workers.dev`
* **Video Demonstration:** [https://youtu.be/ipe4kvTC3fs](https://youtu.be/ipe4kvTC3fs)
