---
title: "Digital Privacy & Security"
type: section-index
id: sec-privacy-security
volatility: periodic
sensitivity: public
tags: [privacy, security, opsec, threat-modeling, encryption, automation]
status: active
last_updated: 2026-01-15
---

# Digital Privacy & Security

This section centralises knowledge, skills, and LLM/MCP-ready automations for:

- **Analyst OPSEC** — protecting sensitive investigations and operator identity
- **Subject privacy auditing** — assessing the digital privacy posture of persons, organisations, and infrastructure encountered in investigations
- **Threat modeling** — structured frameworks for identifying privacy and security risks
- **Automated scanning** — MCP-driven tools for footprint analysis, exposure checks, and privacy scoring

---

## Section Map

| Sub-folder | Contents |
|-----------|---------|
| `knowledge/` | Reference material — frameworks, tool catalogs, protocol references |
| `skills/` | LLM-invocable skills — OPSEC audits, privacy audits, threat modeling |
| `workflows/` | Step-by-step runbooks — pre-op OPSEC, privacy assessment |
| `automations/` | MCP automation configs — footprint scans, exposure checks, metadata analysis |

---

> **Section stub.** This is a section-index for the privacy & security area. The
> sub-folder contents below are illustrative of the full vault's layout and are **not
> included in this training subset**, so they are shown as plain names rather than links.

## Quick Reference

### Knowledge
- `knowledge/threat-modeling` — STRIDE, LINDDUN, PASTA frameworks
- `knowledge/opsec-principles` — OPSEC for threat analysts
- `knowledge/privacy-tools-catalog` — PETs: Tor, VPN, Signal, metadata tools
- `knowledge/encryption-reference` — Algorithms, protocols, key management
- `knowledge/network-privacy` — DNS, Tor, VPN, traffic analysis

### Skills
- `skills/analyst-opsec` — Assess and harden analyst operational security
- `skills/privacy-audit` — Audit privacy posture of a person, org, or infrastructure
- `skills/threat-modeling-skill` — Run a structured threat modeling session

### Workflows
- `workflows/opsec-checklist` — Pre-operation OPSEC verification
- `workflows/privacy-assessment-workflow` — Full privacy assessment runbook
- `workflows/mesh-network-proxy-design` — Strategy for hiding mesh host IPs during OSINT

### Automations
- `automations/mcp-privacy-scan` — MCP-based automated privacy scanning
- `automations/footprint-analysis` — Digital footprint mapping (LLM + MCP)

---

## LLM Integration Points

| Task | LLM | MCP Tools Used |
|------|-----|---------------|
| Footprint analysis | claude-sonnet | mcp__fetch__fetch, mcp__filesystem__write_file |
| Privacy policy parsing | claude-sonnet | mcp__fetch__fetch |
| Threat model generation | claude-sonnet | mcp__filesystem__write_file |
| Metadata extraction | claude-sonnet | mcp__remnux__run_tool (exiftool, mat2) |
| WHOIS/DNS pivot | claude-sonnet | mcp__fetch__fetch (crt.sh, RDAP, DNSDB) |
| OPSEC assessment | claude-sonnet | mcp__filesystem__read_file, mcp__fetch__fetch |

---

## Operational Rules

1. **Investigate — never expose** — privacy audits of subjects must not tip off the subject
2. **Analyst-first** — always assess analyst OPSEC before starting a sensitive investigation
3. **Evidence standard** — every finding must include source, method, and confidence level
4. **TLP:AMBER default** — all privacy investigation outputs are TLP:AMBER unless stated otherwise
5. **No plaintext credentials** — all credential/key references follow the `70-credentials/` masking convention

---

## Integration with Other Vault Sections

| Related Section | Relationship |
|----------------|-------------|
| `10-skills/poi-osint` *(full vault)* | Privacy audits inform and bound POI OSINT scope |
| `10-skills/threat-research-ioc` *(full vault)* | Infrastructure exposure feeds threat actor attribution |
| [[70-credentials/]] | Credential hygiene feeds back into OPSEC checklist (section is `private`) |
