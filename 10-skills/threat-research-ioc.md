---
title: "Threat Research — IOC Enrichment & Pivoting"
type: skill
tags: [threat-research, ioc, virustotal, dnsdb, pivoting, enrichment, campaign-tracking]
llms: [claude-sonnet]
status: active
last_updated: 2026-06-12
source_playbook: /home/user/threat-research/CLAUDE.md
vault_backup: 97-scripts/threat-research/
---

# Threat Research — IOC Enrichment & Pivoting

## Purpose

Systematic IOC enrichment and infrastructure pivoting using VT + DNSDB. Covers indicator triage, deep enrichment, pivot chains, sample collection, threat actor profiling, and MISP event generation.

## Compatible LLMs

| LLM | Notes |
|-----|-------|
| claude-sonnet | Primary |

## Environment Setup

```bash
source /home/user/threat-research-venv/bin/activate
export PATH=$PATH:/home/user/go/bin
# Check enabled APIs:
cat /home/user/threat-research/config/api_keys.json | jq 'to_entries | map(select(.value.enabled == true)) | from_entries | keys'
```

## Scripts

Vault backup: `97-scripts/threat-research/`

| File | Role |
|------|------|
| `97-scripts/threat-research/enrich.py` | IOC enrichment via VT + MISP — single-indicator lookup |

## 6-Phase Process

| Phase | Goal | Primary Tools |
|-------|------|--------------|
| 1 | Initial triage — classify IOC type, quick reputation | `vt file/domain/ip/url` |
| 2 | Deep enrichment — full VT relationships, DNSDB pDNS, Shodan | `vt file {hash} --include=...`, `dnsdb2` |
| 3 | Pivoting & correlation — hash→infra, domain→samples, IP→everything | VT relationships, DNSDB CIDR/reverse |
| 4 | Sample collection | `vt download {sha256}` → `/home/user/threat-research/samples/` |
| 5 | Threat actor / campaign tracking | Actor profile JSON, campaign tracking JSON |
| 6 | Output generation — IOC CSV, STIX 2.1, MISP event, markdown report | PyMISP, stix2 |

## IOC Type Detection

| Pattern | Type | Primary Tool |
|---------|------|-------------|
| 32 hex chars | MD5 | VT |
| 40 hex chars | SHA1 | VT |
| 64 hex chars | SHA256 | VT |
| IPv4 pattern | IPv4 | VT, DNSDB, Shodan |
| `https?://` | URL | VT, URLScan |
| Domain pattern | Domain | VT, DNSDB, WHOIS |

## Key Pivot Chains

```
Hash → VT contacted_domains → DNSDB → Related IPs → More domains
Domain → DNSDB historical IPs → VT communicating_files → Samples
IP → DNSDB reverse → All domains ever hosted
IP → VT communicating_files → All malware using this IP
Email → WHOIS search → Registered domains
```

## Pivot Depth Control

```
MAX_PIVOT_DEPTH = 3
MAX_INDICATORS_PER_LEVEL = 50
```

## Confidence Gate (Workflow Improvements Framework)

| Confidence | Action |
|-----------|--------|
| >70% | PROCEED with operations |
| 50–70% | CONDITIONAL — hypothesis-testing mode |
| <50% | HOLD — do not deploy resources |

## Competing Hypotheses Method

Generate 3–4 alternative hypotheses before committing resources. Score evidence by quality:

- **HIGHEST (95%+):** Multiple independent verified sources
- **HIGH (85%+):** Single high-quality verified source
- **MEDIUM (50–75%):** Corroborating but unverified
- **LOW (<50%):** Circumstantial or single weak indicator

## API Rate Limits

| Service | Rate Limit | Strategy |
|---------|-----------|---------|
| VT Free | 4 req/min | sleep 15 between calls; cache results |
| DNSDB | Per contract | Cache aggressively |
| Shodan | 1/sec | Add delays |

## Sample Handling Rules

1. Never execute samples
2. Store by SHA256 at `/home/user/threat-research/samples/{sha256}/`
3. Always save VT metadata.json with sample
4. Password-protect for sharing: `zip -P infected {sha256}.zip sample.bin`
5. For deep analysis → copy to `/home/user/mcp-lab/incoming/` and run [[10-skills/malware-analysis]]

## Directory Structure

```
/home/user/threat-research/
├── config/api_keys.json
├── investigations/{YYYY-MM-DD}_{case}/
│   ├── scope.json
│   ├── osint/          ← POI OSINT output
│   ├── iocs/
│   ├── samples/
│   ├── enrichment/     ← Cached API results
│   ├── pivots/
│   ├── timeline/
│   └── notes.md
├── samples/{sha256}/
├── iocs/
├── reports/
└── logs/research.log
```

## Tool Gotchas

### PyMISP
- Constructor parameter is `ssl=` not `ssl_verify=`. Common mistake when writing from memory — `ssl_verify=` silently does nothing.
- Tags returned by PyMISP are objects, not strings. Use `.name` to get the string value: `tag.name`, not `str(tag)`. Treating them as strings causes `AttributeError`.
- Target MISP instance: `https://misp.your-org.com`

### Anthropic API — server tool registration
- When registering a native server tool (e.g. `web_search_20250305`), always include an explicit `"name"` field in the tool definition object. Without it the API returns 400 with no descriptive error. Example:
  ```python
  {"type": "web_search_20250305", "name": "web_search", "max_uses": 5}
  ```

### DuckDuckGo search library
- Package renamed from `duckduckgo-search` to `ddgs` at v9.14.1. Old import (`from duckduckgo_search import DDGS`) raises `ModuleNotFoundError` even with the package installed. Use `pip install ddgs` and update imports accordingly.

## Linked Skills

- [[10-skills/malware-analysis]] — deep sample analysis
- [[10-skills/misp-ingestion]] — push enriched IOCs
- [[10-skills/poi-osint]] — for actor attribution phase
