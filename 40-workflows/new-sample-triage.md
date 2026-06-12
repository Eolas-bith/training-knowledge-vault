---
title: "New Sample Triage"
type: workflow
tags: [malware, triage, elf, pe, intake]
llms: [claude-sonnet]
status: active
last_updated: 2026-04-04
---

# New Sample Triage

## Purpose

Fast first-pass triage for unknown samples — identify file type, entropy, packer, and key strings before committing to full analysis.

## Steps

1. **Drop sample** into `/home/user/files/samples/`
2. **Run automated pipeline**:
   ```bash
   python3 /home/user/malware-llm-pipeline/pipeline.py \
       /home/user/files/samples/<sample>
   ```
3. **Review output** at `/home/user/files/output/<sha256>.json`
4. **Decide:**
   - Interesting → review `triage` + `assessment` fields; proceed to deep-dive if warranted
   - Duplicate → VT `vt_detection_ratio` and `vt_first_seen` will confirm; archive
   - Benign → `assessment` field will indicate; log and discard

## Sample Drop Location

| Purpose | Path |
|---------|------|
| **Primary (pipeline input)** | `/home/user/files/samples/` |
| Legacy / mcp-lab | `/home/user/mcp-lab/incoming/` *(old — prefer files/samples)* |

## Pipeline Output Location

```
/home/user/files/output/<sha256>.json
```

## Quick Triage via JSON Fields

| Field | What to check |
|-------|--------------|
| `triage` | File structure anomalies, obfuscation indicators |
| `vt_metadata.vt_detection_ratio` | Community detection rate |
| `mitre` | ATT&CK techniques — count and tactic coverage |
| `strings.crypto_constants` | Crypto library presence (LibTomCrypt, OpenSSL etc.) |
| `sections` | Suspicious entropy sections |
| `iocs` | Network indicators — if empty, check for dynamic C2 |
| `functions_table` | Function count by classification (crypto/network/evasion) |

## LLM Routing

| Step | LLM | Reason |
|------|-----|--------|
| Full pipeline | claude-sonnet | Tool access + synthesis |
| Family attribution | claude-sonnet | Long context |
| Report review | gpt-4o (optional) | Second opinion |

## Linked Skills

- [[10-skills/malware-analysis]]
- [[40-workflows/malware-llm-pipeline]]
- [[10-skills/yara-generation]]

## Notes

- `ANTHROPIC_API_KEY` and `VT_API_KEY` must be set in `/home/user/malware-llm-pipeline/.env`
- REMnux MCP runs locally (local connector mode) — all tools are on the analyst machine
- Use `--no-vt` flag if VT lookup not needed or key unavailable
- Check `functions_table[].classification` counts: high crypto + network + low unknown = sophisticated sample
