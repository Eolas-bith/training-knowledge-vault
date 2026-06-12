<img width="1536" height="1024" alt="Knowledge Vault" src="assets/vault-header.png" />

# Training Knowledge Vault

> A blueprint for structuring analytical knowledge so that both humans and AI can use it reliably.

---

## What is this?

This is a **training version of a structured knowledge vault** — an open blueprint for how to organise methodology, prompts, and analytical procedures so they can be used by an analyst, an LLM, or both working together.

It is not a wiki. It is not a note collection. It is a deliberately structured system where every piece of knowledge has a type, a location, and a relationship to the work it supports.

The vault follows one core idea: **if you write your methodology clearly, an AI agent can follow it just as reliably as a human colleague — and improve it over time through a structured feedback loop.**

---

## Who is this for?

**Analysts and researchers** who want a reproducible system for capturing methodology — not just notes. If you have ever finished an investigation, learned something important, and then forgotten it before the next one, this vault architecture solves that problem.

**Teams** building agentic AI workflows. The vault is the instruction layer that sits between a human operator and an LLM. Skill files tell the agent exactly what to do. Prompt files are the trigger. Workflow files chain them into pipelines. Session logs close the feedback loop.

**Anyone learning how to work with AI agents productively.** The most important lesson in this vault is that an LLM's output quality is determined almost entirely by the quality of the instructions it receives. This vault is an architecture for writing those instructions well, maintaining them over time, and improving them from operational experience.

---

## The core concept: structured instructions for agentic AI

A typical LLM interaction looks like this: you describe a task, the LLM improvises an approach, you get a result that may or may not be reliable. This works for simple tasks. It fails for complex multi-step analytical work where consistency, auditability, and accumulated expertise matter.

The vault solves this by replacing improvisation with structured methodology:

```
30-prompts/          ← you trigger a skill with a prompt
      ↓
10-skills/           ← the skill tells the agent exactly what to do and how
      ↓
40-workflows/        ← workflows chain skills into end-to-end pipelines
      ↓
60-sessions/         ← sessions log what happened and what was learned
      ↓
00-index/lessons-log ← lessons accumulate and feed back into skill files
```

Each cycle makes the skill files more accurate. Over time the vault becomes a codification of real operational expertise that any LLM can follow without improvisation.

---

## What is in this vault?

### `10-skills/` — Analytical skill files

The heart of the vault. One file per analytical capability. Each skill file contains:
- **Purpose** — what this skill does and when to use it
- **Required inputs** — what context the agent needs before starting
- **Procedure** — step-by-step, with exact tool invocations where relevant
- **Output format** — what a completed run produces
- **Notes** — edge cases, known failure modes, lessons learned

A skill file is what you give an LLM instead of improvised instructions. It is the difference between "do a malware analysis" and a documented, reproducible procedure.

**In this training vault:** `vault-curation.md` — the meta-skill that governs how the vault itself is maintained. Read this first. `_template.md` — the blank template for adding your own skills.

### `30-prompts/` — Prompt templates

The text you use to trigger a skill in an LLM. A good prompt template:
- Specifies the skill file to read first
- Provides variable placeholders (`{SAMPLE_PATH}`, `{TARGET_NAME}`) so the same prompt works across cases
- Defines the expected output format so the LLM produces structured, parseable results

**In this training vault:** `vault-distillation-prompt.md` — the prompt that drives a lessons distillation run (Phase 2 of vault curation). `_template.md` — blank template.

### `40-workflows/` — Multi-step runbooks

When an investigation requires more than one skill — for example: enrich IOCs, then build a threat actor profile, then draft a report — a workflow coordinates the sequence. Workflows define phases, inputs, outputs, and quality gates.

**In this training vault:** `_template.md` — blank template showing the workflow structure.

### `50-knowledge/` — Reference knowledge

Structured reference material that skills and workflows can read from. Includes:

- **`threat-actors/_template.md`** — full threat actor profile structure: identity, victimology, modus operandi, ATT&CK mapping, atomic indicators
- **`malware-families/_template.md`** — malware family documentation template
- **`knowledge-graphs/`** — theory and practice of building knowledge graphs for analytical work
- **`ontology-and-llm.md`** — why ontologies matter for AI work: how structured schemas prevent hallucination, how STIX 2.1 and MITRE ATT&CK model knowledge, how to design extraction pipelines that produce consistent, auditable results

### `60-sessions/` — Session logs

A dated log of every significant piece of analytical work. Sessions serve two purposes: they are the lab notebook of record, and they are the raw material that feeds vault curation.

Each session has a `## Flagged Observations` section where unexpected findings are recorded — not as lessons, but as candidates for later analyst review. This is deliberate: an LLM cannot reliably determine root cause, so observations are captured and a human decides in a later curation pass whether they are genuine and worth incorporating into methodology.

**In this training vault:** `_template.md` — the session template with full frontmatter schema. Two synthetic example sessions showing the format.

### `20-llm-configs/` and `22-personas/` — LLM configuration

One file per LLM provider, documenting endpoint, model ID, context window, cost tier, strengths, and weaknesses. Personas define behavioural contracts — what to reliably expect from an LLM in a given role, and what it will not do.

### `70-credentials/` — Credential inventory

This section holds masked references and config file paths — never plaintext secrets. The format shows which environment variable to set, which config file holds the value, and when the credential was last rotated. The actual secret stays in its canonical config file outside the vault.

### `97-scripts/` — Pipeline scripts

Canonical copies of automation scripts that implement vault workflows. The vault is source of truth; runtime hosts are deployments. Every script maps to a skill file and a workflow — the README explains the full mapping chain.

---

## How ontology shapes everything

The `50-knowledge/ontology-and-llm.md` file is worth reading even if you never build a knowledge graph. It explains the foundational reason why structured knowledge vaults work better than unstructured notes for AI-assisted work:

An LLM has no persistent model of relationships between things. It generates text from statistical patterns. When you give it a well-defined schema — entity types, relation labels, provenance requirements — it can extract structured, verifiable, mergeable information instead of plausible-sounding but unauditable prose.

The same principle applies to skill files, prompt templates, and workflow runbooks. The more precisely you define what the agent should do, what schema it should produce, and what counts as done, the more reliably it performs.

---

## Getting started

**As a human — Obsidian:**
1. Open this directory as an Obsidian vault
2. Install the **Dataview** plugin
3. Start at `00-index/HOME.md`

**With Claude Code:**
1. `cd` into this directory and open a Claude Code session
2. `CLAUDE.md` is loaded automatically — the LLM knows what the vault is
3. Ask it to read a skill file and follow it: `"Read 10-skills/vault-curation.md and explain the four phases"`

**Building your own vault:**
1. Fork this repo
2. Read `10-skills/vault-curation.md` — it defines the maintenance system
3. Copy `10-skills/_template.md` to start your first skill file
4. Add skills as you do work; log sessions; run a curation pass after every 5 sessions

---

## Key rules

| Rule | Reason |
|------|--------|
| Skill files are not touched during analysis | Editing methodology mid-investigation creates drift; use the curation process |
| Sessions are append-only | Past sessions are the audit trail; add new ones, never edit old |
| Credentials are masked | The vault may be shared; secrets belong in config files, not here |
| Prompts are specific | Vague prompts produce improvised outputs; specificity is the defence against hallucination |
| Observations are flagged, not immediately written as lessons | LLMs cannot reliably diagnose root cause; humans review first |

---

<img width="1536" height="1024" alt="Knowledge Vault" src="assets/vault-footer.png" />
