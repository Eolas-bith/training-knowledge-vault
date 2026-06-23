# Training Knowledge Vault — Agent Instructions

> This is a training version of a knowledge vault, designed to demonstrate vault architecture and methodology. It contains sanitised, realistic content drawn from operational practice. No real credentials, IPs, or personal information are present.

This is the **canonical, tool-neutral instruction file** for this vault. It is written to be read by any coding/agent tool — Codex, Claude Code, Google Antigravity, Gemini CLI, or a local model run through Ollama / LM Studio. See [Using this vault with any AI tool](#using-this-vault-with-any-ai-tool) for how each tool loads it.

---

## Using this vault with any AI tool

This vault keeps one source of truth — **this file (`AGENTS.md`)** — and provides thin adapter files for tools that look for a different name. Edit `AGENTS.md`; the adapters point back to it, so there is no second copy to keep in sync.

| Tool | What it reads | How it gets these instructions |
|------|---------------|--------------------------------|
| **Codex** (OpenAI) | `AGENTS.md` | Native — reads this file directly. |
| **Google Antigravity** | `AGENTS.md` + `GEMINI.md` | Native — reads this file; `GEMINI.md` holds only Antigravity/Gemini-specific overrides. |
| **Gemini CLI** | `GEMINI.md` (default) | `.gemini/settings.json` sets `context.fileName` to load `AGENTS.md` too. |
| **Claude Code** | `CLAUDE.md` | `CLAUDE.md` imports this file via `@AGENTS.md` (expanded inline at session start). |
| **Ollama / LM Studio** (and other local runners) | *no file convention* | Load this file's contents as the system prompt / context manually. See below. |

**Local models (Ollama, LM Studio, llama.cpp, and agent frontends like Continue / Cline / opencode):** these are plain inference runners with no auto-loaded context file. This file is plain Markdown — paste it as the **system prompt**, or point your frontend's "rules"/"context" setting at `AGENTS.md`. A minimal bootstrap prompt: *"Read AGENTS.md in the vault root, then follow its navigation and rules before doing any task."* Tool-specific behaviour (auto-loading, `@imports`, slash commands) does **not** apply here — everything in this file is written to work from a plain context window.

> **Keep instructions tool-neutral.** Anything in this file should make sense to *any* model. Put genuinely tool-specific behaviour in that tool's adapter file (`CLAUDE.md`, `GEMINI.md`), never here.

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
| Canonical frontmatter schema (field definitions) | `00-index/frontmatter-schema.md` |
| Validate vault structure (run before committing) | `97-scripts/vault-doctor.py` |
| How to run a specific investigation | `10-skills/{skill-name}.md` |
| What prompt to use | `30-prompts/{prompt-name}.md` |
| Multi-step runbook | `40-workflows/{workflow-name}.md` |
| Which LLM to use | `20-llm-configs/{llm-name}.md` |
| AI persona profiles (behavioral contracts) | `22-personas/{persona-name}.md` |
| Known malware families | `50-knowledge/malware-families/` |
| Threat actor profiles | `50-knowledge/threat-actors/` |
| Ontology / knowledge representation for AI | `50-knowledge/ontology-and-llm.md` |
| Knowledge graph theory and extraction pipelines | `50-knowledge/knowledge-graphs/` |
| API keys / SSH hosts | `70-credentials/` |
| Digital privacy & security (OPSEC, audits, threat modeling) | `80-privacy-security/README.md` |
| Analyst identity and collaboration rules | `81-profile/README.md` |
| Canonical pipeline scripts (source of truth) | `97-scripts/README.md` |
| Session template (canonical frontmatter schema) | `60-sessions/_template.md` |
| LLM config guide | `20-llm-configs/README.md` |

---

## Frontmatter fields (machine-readable)

Canonical definitions live in `00-index/frontmatter-schema.md` and are enforced by
`97-scripts/vault-doctor.py`. Every file (except the root instruction files —
`AGENTS.md`, `CLAUDE.md`, `GEMINI.md` — and `README.md`) has:
- `title:` — human-readable name
- `id:` — **stable, globally-unique slug that never changes, even if the file moves.**
  Cross-references that must survive reorganisation — especially from append-only
  sessions — record the `id`, not the path. Convention: `<section-prefix>-<slug>`
  (e.g. `kb-ontology-and-llm`, `skill-vault-curation`).
- `type:` — `skill | prompt | llm-config | persona | workflow | reference | session | index | section-index | session-index`
- `status:` — `active | draft | deprecated | in-progress | complete`
- `volatility:` — `stable | periodic | volatile` (how often it changes; drives where it belongs)
- `sensitivity:` — `public | internal | private` (who may load it; machine-checked segregation)
- `tags:` — topic list
- `llms:` — which LLMs this applies to *(optional)*
- `source_playbook:` — canonical source file on disk *(skill files only)*

---

## Rules for agents using this vault

0. **Profile section: see `81-profile/` for analyst identity and collaboration rules.** Load only when the user explicitly requests voice/style output — e.g., "write this in my voice", "use my style". Skip for all technical analysis tasks. See `81-profile/README.md` for the full loading policy.

1. **Read the relevant skill file before starting any investigation.** Skills contain tool chains, commands, output formats, and lessons learned — do not improvise what is already documented.

2. **Check `50-knowledge/investigations-index.md` before starting any investigation** — the case may have been worked before with existing artifacts.

3. **Do not modify vault files during an investigation** unless explicitly asked. Vault files are methodology — update them only to add genuine lessons learned or fix errors.

4. **Log session activity in `60-sessions/YYYY-MM-DD-session.md`** if doing significant work from this vault context.

5. **Flag candidate observations in `## Flagged Observations` — do not write lessons.** Record what happened, what was observed, and what was directly tried and confirmed. Do **not** diagnose root causes or assert fixes that were not verified within the session — an LLM cannot reliably distinguish a tool failure from a usage error from an environment issue. Flag the symptom; the analyst decides in Phase 3 of vault curation whether the observation is genuine, what caused it, and whether it becomes permanent methodology. See `10-skills/vault-curation.md` for the format.

6. **Credentials rule:** `70-credentials/` holds masked values and paths only. Never look for plaintext secrets here — check the canonical config files listed in the inventory.

7. **Source playbooks:** Skill files with `source_playbook:` frontmatter are summaries. If you need the full original playbook (e.g., for step-by-step commands), read the source file directly.

8. **Dataview blocks are Obsidian-only.** Any ` ```dataview ``` ` block is rendered dynamically by the Obsidian plugin and is an empty/unreadable code block in CLI and agent contexts. Do not rely on them for navigation. Use these fallbacks instead:
   - **Skills list:** Read `00-index/skills-index.md` → `## By Domain` static section, or: `grep -r "^title:" 10-skills/ | grep -v _template`
   - **LLM configs:** Read `00-index/llm-config-index.md` → `## Available Configs` static table, or: `grep -r "^title:" 20-llm-configs/ | grep -v _template`
   - **Prompts:** `grep -rl "type: prompt" 30-prompts/*.md | grep -v deprecated`
   - **Sessions:** Read `60-sessions/SESSION_INDEX.md`
   - **Skills by LLM:** `grep -rl "claude-sonnet" 10-skills/` / `grep -rl "gpt-4o" 10-skills/`

9. **Reference files by `id`, not path, in anything append-only.** Sessions and the
   investigations index are append-only, so a hard-coded path freezes the structure:
   moving a knowledge file would silently break historical links. Record the target's
   stable `id` (and an optional wikilink for humans). This is what lets the vault be
   reorganised without rewriting the audit trail.

10. **Run `97-scripts/vault-doctor.py` before committing structural changes.** It enforces
   frontmatter, the type/volatility/sensitivity enums, id uniqueness, nav parity, link
   integrity, and the public↛private segregation boundary. A pre-commit hook
   (`.githooks/pre-commit`) and CI (`--strict`) run it automatically; run it by hand after
   adding files, moving things, or editing this file.

---

## Quick skill selection guide

| Task | Where to go |
|------|-------------|
| Understand how the vault maintains itself | `10-skills/vault-curation.md` |
| Count tokens in an agent context file (AGENTS.md / CLAUDE.md) or skill file / optimize system prompt length | `50-knowledge/system-prompt-token-management.md` |
| Trim or calibrate the context file per model (token budget, evals, session lifecycle) | `10-skills/vault-curation.md` → `## Context-File Maintenance` |
| Add a new skill to the vault | `10-skills/_template.md` |
| Add a new prompt | `30-prompts/_template.md` |
| Add a new workflow | `40-workflows/_template.md` |
| Run a lessons distillation pass | `30-prompts/vault-distillation-prompt.md` |
| Understand ontologies and why they matter for AI | `50-knowledge/ontology-and-llm.md` |
| Build or extend a knowledge graph | `50-knowledge/knowledge-graphs/README.md` |
| Profile a threat actor | `50-knowledge/threat-actors/_template.md` |
| Document a malware family | `50-knowledge/malware-families/_template.md` |
| Look up credential config paths | `70-credentials/api-keys-inventory.md` |
| Understand how scripts map to skills | `97-scripts/README.md` |
| Log a session | `60-sessions/_template.md` |
| See example sessions | `60-sessions/analysis-server/` |
