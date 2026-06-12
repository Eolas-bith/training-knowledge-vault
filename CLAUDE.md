# Training Knowledge Vault — LLM Instructions

> This is a training version of a CTI/OSINT knowledge vault, designed to demonstrate vault architecture and methodology. It contains sanitised, realistic content drawn from operational practice. No real credentials, IPs, or personal information are present.

This file is loaded automatically by Claude Code when this vault is the working directory.

---

## What this vault is

A structured knowledge base for threat analysis, OSINT, and narrative intelligence work. It contains methodology (skills, prompts, workflows), LLM configuration profiles, reference knowledge (malware families, case index), and a credentials inventory.

It is **not** a project workspace. Samples, reports, and runtime artifacts live in separate working directories:
- `/home/user/mcp-lab/` — malware analysis runs
- `/home/user/threat-research/` — IOC enrichment, OSINT investigations
- `/home/user/writing/` — reports, papers, thesis chapters

---

## How to navigate

| Need | Go to |
|------|-------|
| What skills exist | `00-index/skills-index.md` |
| How to run a specific investigation | `10-skills/{skill-name}.md` |
| What prompt to use | `30-prompts/{prompt-name}.md` |
| Multi-step runbook | `40-workflows/{workflow-name}.md` |
| Which LLM to use | `20-llm-configs/{llm-name}.md` |
| AI persona profiles (behavioral contracts) | `22-personas/{persona-name}.md` |
| Past cases / investigation index | `50-knowledge/investigations-index.md` |
| OSAI (AI-300) cert prep | `50-knowledge/osai/` |
| Known malware families | `50-knowledge/malware-families/` |
| Threat actor profiles | `50-knowledge/threat-actors/` |
| Behavioral analysis methods (7 traditions) | `50-knowledge/behavioral-analysis/` |
| Detection engineering (SIEM rules, ATT&CK coverage, suppression) | `50-knowledge/detection-engineering/` |
| API keys / SSH hosts | `70-credentials/` |
| Profile section | `81-profile/` — see README for analyst identity and collaboration rules |
| Canonical pipeline scripts (source of truth) | `97-scripts/` |
| Platform takedown / remediation scenarios | `50-knowledge/takedown-remediation-matrix.md` |
| MISP-MCP platform setup and rebuild | `50-knowledge/tools/misp-mcp-setup.md` |
| Session template (canonical frontmatter schema) | `60-sessions/_template.md` |
| LLM config vs model-map boundary | `20-llm-configs/README.md` |

---

## Frontmatter fields (machine-readable)

Every file has:
- `type:` — `skill | prompt | llm-config | persona | workflow | reference | session`
- `tags:` — topic list
- `llms:` — which LLMs this applies to
- `status:` — `active | draft | deprecated`
- `source_playbook:` — canonical source file on disk (skill files only)

---

## Rules for LLMs using this vault

0. **Profile section: see `81-profile/` for analyst identity and collaboration rules.** Load only when the user explicitly requests voice/style output — e.g., "write this in my voice", "use my style". Skip for all technical analysis tasks. See `81-profile/README.md` for the full loading policy.

1. **Read the relevant skill file before starting any investigation.** Skills contain tool chains, commands, output formats, and lessons learned — do not improvise what is already documented.

2. **Check `50-knowledge/investigations-index.md` before starting any investigation** — the case may have been worked before with existing artifacts.

3. **Do not modify vault files during an investigation** unless explicitly asked. Vault files are methodology — update them only to add genuine lessons learned or fix errors.

4. **Log session activity in `60-sessions/YYYY-MM-DD-session.md`** if doing significant work from this vault context.

5. **Flag candidate observations in `## Flagged Observations` — do not write lessons.** Record what happened, what was observed, and what was directly tried and confirmed. Do **not** diagnose root causes or assert fixes that were not verified within the session — an LLM cannot reliably distinguish a tool failure from a usage error from an environment issue. Flag the symptom; the analyst decides in Phase 3 of vault curation whether the observation is genuine, what caused it, and whether it becomes permanent methodology. See `10-skills/vault-curation.md` for the format.

6. **Credentials rule:** `70-credentials/` holds masked values and paths only. Never look for plaintext secrets here — check the canonical config files listed in the inventory.

7. **Source playbooks:** Skill files with `source_playbook:` frontmatter are summaries. If you need the full original playbook (e.g., for step-by-step commands), read the source file directly.

8. **Dataview blocks are Obsidian-only.** Any ` ```dataview ``` ` block is rendered dynamically by the Obsidian plugin and is an empty/unreadable code block in CLI and MCP contexts. Do not rely on them for navigation. Use these fallbacks instead:
   - **Skills list:** Read `00-index/skills-index.md` → `## By Domain` static section, or: `grep -r "^title:" 10-skills/ | grep -v _template`
   - **LLM configs:** Read `00-index/llm-config-index.md` → `## Available Configs` static table, or: `grep -r "^title:" 20-llm-configs/ | grep -v _template`
   - **Prompts:** `grep -rl "type: prompt" 30-prompts/*.md | grep -v deprecated`
   - **Sessions:** Read `60-sessions/SESSION_INDEX.md` or `~/.claude/SESSION_INDEX.md`
   - **Skills by LLM:** `grep -rl "claude-sonnet" 10-skills/` / `grep -rl "gpt-4o" 10-skills/`

---

## Quick skill selection guide

| Task | Skill |
|------|-------|
| Write / review / tune SIEM detection rules | `10-skills/detection-engineering.md` |
| Draft a new detection rule (templates by input type) | `50-knowledge/detection-engineering/detection-rule-templates.md` |
| Windows LOLBin / process chain detection patterns | `50-knowledge/detection-engineering/lolbins-process-patterns.md` |
| Linux GTFOBins / reverse shell / container escape patterns | `50-knowledge/detection-engineering/linux-process-patterns.md` |
| Windows Security Event ID reference | `50-knowledge/detection-engineering/windows-event-ids.md` |
| Suricata / Snort rule syntax | `50-knowledge/detection-engineering/suricata-snort-syntax.md` |
| ATT&CK technique → rule coverage lookup | `50-knowledge/detection-engineering/att-ck-coverage-map.md` |
| Rule quality metrics / tuning decision tree | `50-knowledge/detection-engineering/rule-quality-metrics.md` |
| Suppression pattern reference | `50-knowledge/detection-engineering/suppression-patterns.md` |
| Analyse malware samples (ELF/Linux) | `10-skills/malware-analysis.md` |
| Analyse Windows PE (manual reversing) | `10-skills/windows-pe-reversing.md` |
| x86/x64 assembly reference | `50-knowledge/re-fundamentals.md` |
| Windows API patterns for RE | `50-knowledge/windows-api-malware.md` |
| Generate YARA rules | `10-skills/yara-generation.md` |
| Enrich IOCs (VT, DNSDB, pivoting) | `10-skills/threat-research-ioc.md` |
| Push IOCs to MISP | `10-skills/misp-ingestion.md` |
| Investigate a person (OSINT) | `10-skills/poi-osint.md` |
| Investigate media influence operation | `10-skills/influence-ops-media.md` |
| Compound court/media/actor investigation | `10-skills/narrative-threat-actor.md` |
| Apply SATs, ACH, or Red Team analysis | `10-skills/structured-analytical-techniques.md` |
| Map intrusion via Diamond Model / ATT&CK | `10-skills/structured-analytical-techniques.md` |
| Threat model a system (STRIDE, PASTA, LINDDUN) | `10-skills/threat-modeling.md` |
| Quantify risk (FAIR, Monte Carlo, NIST RMF) | `10-skills/quantitative-risk-management.md` |
| Write threat report / security blog | `85-writing/infosec-report-writing.md` |
| Write academic paper / conference submission | `85-writing/academic-writing.md` |
| Distil session lessons → skill files | `10-skills/vault-curation.md` |
| Take down fake profile / phishing domain / leaked creds | `50-knowledge/takedown-remediation-matrix.md` |
