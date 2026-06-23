---
title: "Home"
type: index
id: idx-home
tags: [index]
status: active
volatility: periodic
sensitivity: public
last_updated: 2026-06-23
---

# Knowledge Vault

> A structured knowledge base for threat analysis, OSINT, and intelligence work.

## Navigation

| Folder | Purpose |
|--------|---------|
| [[skills-index]] | Skills and capabilities catalogue |
| [[llm-config-index]] | LLM configuration profiles |
| [[22-personas/README\|22-personas/]] | AI persona profiles — behavioral contracts, trust boundaries, interaction notes |
| [[30-prompts/]] | Reusable prompt templates |
| [[40-workflows/]] | Multi-step analysis workflows |
| [[50-knowledge/investigations-index]] | All investigations — malware, CTI, OSINT research |
| [[50-knowledge/tools/]] | Tool reference notes |
| [[60-sessions/]] | Dated session notes |
| [[70-credentials/]] | API keys, SSH config (section is `private`) |
| [[80-privacy-security/README]] | Digital privacy & security — OPSEC, audits, threat modeling |

---

## Quick Links

- [[80-privacy-security/README]] — Privacy & security section hub
- [[40-workflows/_template]] — Add a multi-step workflow
- [[10-skills/_template]] — Add a new skill
- [[20-llm-configs/_template]] — Add a new LLM config
- [[22-personas/_template]] — Add a new persona
- [[30-prompts/_template]] — Add a new prompt

---

## Dataview — Active Skills

<!-- LLM: Obsidian Dataview block below — not rendered in CLI/MCP. For skills, read 00-index/skills-index.md → ## By Domain, or: grep -r "^title:" 10-skills/ | grep -v _template -->
```dataview
TABLE llms, tags, status
FROM "10-skills"
WHERE status = "active"
SORT title ASC
```

## Dataview — All Prompts by LLM

<!-- LLM: Obsidian Dataview block below — not rendered in CLI/MCP. For prompts: grep -rl "type: prompt" 30-prompts/ | grep -v deprecated -->
```dataview
TABLE title, tags, status
FROM "30-prompts"
WHERE type = "prompt"
SORT title ASC
```
