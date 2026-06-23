---
title: "API Keys Inventory"
type: reference
id: cred-api-keys-inventory
volatility: volatile
sensitivity: private
publish: true
tags: [credentials, api-keys]
status: active
last_updated: 2026-01-15
---

# API Keys Inventory

All values are masked. Actual secrets live in the canonical `.env` files listed per entry. Never commit raw key values to git.

---

## LLM Providers

### Anthropic (Claude)

| Field | Value |
|-------|-------|
| Key name | `ANTHROPIC_API_KEY` |
| Masked value | `sk-ant-••••••••` |
| Canonical location | `/home/user/malware-llm-pipeline/.env` |
| Console | https://console.anthropic.com → API Keys |
| Status | Active |
| Last rotated | — |

### OpenAI

| Field | Value |
|-------|-------|
| Key name | `OPENAI_API_KEY` |
| Masked value | `sk-proj-••••••••` |
| Canonical location | `/home/user/malware-llm-pipeline/.env` |
| Console | https://platform.openai.com → API Keys |
| Status | Active |
| Last rotated | — |

### OpenRouter

| Field | Value |
|-------|-------|
| Key name | `OPENROUTER_API_KEY` |
| Masked value | `sk-or-v1-••••••••` |
| Canonical location | `/home/user/malware-llm-pipeline/.env` |
| Console | https://openrouter.ai/keys |
| Status | Active |
| Last rotated | — |

### Google AI (Gemini)

| Field | Value |
|-------|-------|
| Key name | `GOOGLE_API_KEY` |
| Masked value | `AIza••••••••` |
| Canonical location | `/home/user/malware-llm-pipeline/.env` |
| Console | https://aistudio.google.com → API Keys |
| Status | Active |
| Last rotated | — |

---

## Threat Intelligence

### VirusTotal Enterprise

| Field | Value |
|-------|-------|
| Key name | `VT_API_KEY` |
| Masked value | `••••••••` |
| Canonical location | `/home/user/malware-llm-pipeline/.env` |
| Console | https://www.virustotal.com/gui/user/[your-username]/apikey |
| Status | Active |
| Last rotated | — |

### DNSDB (Farsight)

| Field | Value |
|-------|-------|
| Key name | `DNSDB_API_KEY` |
| Masked value | `••••••••` |
| Canonical location | `/home/user/.env` |
| Console | https://api.dnsdb.info |
| Status | Active |
| Last rotated | — |

### Semantic Scholar

| Field | Value |
|-------|-------|
| Key name | `SEMANTIC_SCHOLAR_API_KEY` |
| Masked value | `••••••••` |
| Canonical location | `/home/user/.env` |
| Console | https://www.semanticscholar.org/product/api |
| Status | Pending |
| Last rotated | — |

---

## Platform APIs

### MISP

| Field | Value |
|-------|-------|
| Key name | `MISP_API_KEY` |
| Masked value | `••••••••` |
| Canonical location | `/home/user/cti-pipeline/.env` |
| Instance URL | `https://misp.your-org.com` |
| Status | Active |
| Last rotated | — |

---

## Notes

- **Rotation trigger:** Any key committed to git — even briefly — must be considered compromised and rotated immediately. Check `git log --all` and `git reflog` after any accidental exposure.
- **`.env` files** must be listed in `.gitignore` in every project directory. Verify with `git check-ignore -v .env`.
- **Backup:** Encrypt canonical `.env` files with GPG and store the encrypted archive externally. See `70-credentials/README.md` for the backup procedure.
