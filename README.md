# CTI/OSINT Knowledge Vault

A structured, methodology-first knowledge base for threat analysis, OSINT, and narrative intelligence work. This vault organises operational knowledge into a format that both human analysts and LLMs can use effectively.

---

## What is a knowledge vault?

A knowledge vault is a personal or team knowledge base that stores methodology alongside context. Unlike a wiki or note collection, a vault has:

- **Skill files** — step-by-step procedures for specific analytical tasks (malware analysis, IOC enrichment, OSINT)
- **Prompt templates** — reusable LLM prompts that encode best practices and prevent common errors
- **Workflows** — multi-step runbooks that coordinate several skills into end-to-end pipelines
- **Reference knowledge** — threat actor profiles, malware family data, detection engineering rules
- **Session logs** — dated records of actual work, feeding a continuous improvement loop

The vault is the **source of truth** for methodology. Runtime artifacts (samples, reports, IOC lists) live in separate working directories and are referenced from sessions. The vault itself stays clean and versionable.

---

## Why use one?

**For humans:** Structured methodology prevents "starting from scratch" on every investigation. When you encounter an edge case — a tool that fails silently, a false positive pattern, a better pivot sequence — you capture it once and it becomes part of how all future work is done.

**For LLMs:** A well-structured vault dramatically reduces hallucination during agentic workflows. Instead of the LLM improvising a malware analysis pipeline from training data, it reads `10-skills/malware-analysis.md` and follows documented procedures with known-good tool invocations and error handling.

**Together:** The vault curation loop (capture → aggregate → review → apply) means lessons from sessions gradually improve the skill files over time, without requiring manual methodology rewrites.

---

## Directory structure

```
00-index/           Navigation, skill index, LLM config index, lessons log, curation log
10-skills/          Skill files — one per analytical capability
20-llm-configs/     Per-provider API config (endpoint, model, cost tier, quirks)
22-personas/        LLM persona profiles — behavioral contracts and trust boundaries
30-prompts/         Reusable prompt templates
40-workflows/       Multi-step runbooks that chain skills together
50-knowledge/       Reference knowledge — malware families, threat actors, detection engineering
60-sessions/        Dated session logs and session index
70-credentials/     Masked credential inventory and SSH config (no plaintext secrets)
75-remote-orchestration/  Distributed worker architecture notes
80-privacy-security/ OPSEC principles, privacy audit workflows, threat modeling
81-profile/         Analyst identity, voice, and LLM collaboration rules (optional)
85-writing/         Writing skills — infosec reports, academic papers
97-scripts/         Canonical pipeline scripts (vault is source of truth)
```

Each directory has a `README.md` explaining what belongs there and how to use it.

---

## How Claude Code and Obsidian use this vault

**Obsidian** is the primary UI. It renders wikilinks (`[[file-name]]`), runs Dataview queries for dynamic indexes, and provides graph view for exploring connections. The `.obsidian/` directory holds configuration.

**Claude Code** reads the vault as a filesystem. When you open a terminal in this directory, `CLAUDE.md` is loaded automatically and tells the LLM what the vault is. Skill files, prompts, and session logs are all plain Markdown — the LLM reads them directly.

**Important:** Dataview blocks (`\`\`\`dataview\`\`\``) only render in Obsidian. Claude Code sees them as empty code blocks. The vault maintains static fallbacks in every index file — these are the LLM-readable versions.

---

## How to get started

### Add a new skill

1. Copy `10-skills/_template.md` to `10-skills/your-skill-name.md`
2. Fill in the frontmatter (title, type, tags, llms, status, last_updated)
3. Write the Purpose, Required Context, Prompt Template, and Output Format sections
4. Link it from `00-index/skills-index.md` under the appropriate domain

### Log a session

1. Copy `60-sessions/_template.md` to `60-sessions/your-host/YYYY-MM-DD-topic.md`
2. Fill in the frontmatter and write the Objective, Completed, and Key Findings sections
3. If you observe something unexpected, add a `## Flagged Observations` section using the format in the template
4. Append an entry to `60-sessions/SESSION_INDEX.md`

### Run a curation pass

1. Read `10-skills/vault-curation.md` — it defines the four-phase process
2. When 5+ sessions have accumulated since the last run, trigger a distillation run using `30-prompts/vault-distillation-prompt.md`
3. The distillation run reads sessions → writes to `00-index/lessons-log.md` (skill files are **not** touched)
4. Review the lessons log and explicitly nominate lessons to apply
5. Update `00-index/vault-curation-log.md` with the run record

### Do an investigation

1. Check `50-knowledge/investigations-index.md` — the case may have prior work
2. Read the relevant skill file (e.g., `10-skills/malware-analysis.md`)
3. Work in a separate directory outside the vault
4. Log your session in `60-sessions/`

---

## Key design principles

- **Vault is methodology; working dirs are artifacts.** Never commit samples, reports, or live IOC data to the vault.
- **Skill files are not touched during analysis.** Only updated via the explicit curation process.
- **Sessions are append-only.** Don't edit past sessions; add new ones.
- **Credentials are masked.** `70-credentials/` holds paths and masked values; actual secrets stay in their canonical config files.
- **LLMs read what you write.** If a skill file is vague, the LLM will improvise. Specificity in skill files is the primary defence against hallucination in agentic workflows.
