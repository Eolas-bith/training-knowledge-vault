<img width="1536" height="1024" alt="Knowledge Vault" src="assets/vault-header.png" />

# Training Knowledge Vault

> A blueprint for structuring analytical knowledge so that both humans and AI can use it reliably.

---

## What is this?

This is a **training version of a structured knowledge vault** — an open blueprint for how to organise methodology and reference knowledge so they can be used by an analyst, an LLM agent, or both working together.

It is not a wiki. It is not a note collection. It is a deliberately structured system where every piece of knowledge has a type, a location, and a clear relationship to the work it supports.

The vault follows one core idea: **if you write your methodology clearly, an AI agent can follow it just as reliably as a human colleague — and improve it over time through a structured feedback loop.**

---

## The fundamental distinction: Knowledge vs Skills

Most knowledge management systems treat all information as the same kind of thing. This vault makes a hard distinction that matters enormously when AI is involved.

### Knowledge (`50-knowledge/`) — what you know

Knowledge files are **reference material**. They describe the world: what a thing is, how it works, what its properties are. Knowledge is read by skills and workflows; it is not itself a procedure.

Examples of knowledge:
- A profile of a subject or entity (who they are, what they do, what is known about them)
- A taxonomy or classification scheme
- A reference table of standards, codes, or identifiers
- Domain background: definitions, historical context, key concepts
- An ontology: how entities in a domain relate to each other

Knowledge files answer the question: **"what do I need to know about X?"**

### Skills (`10-skills/`) — how you do things

Skill files are **procedural methodology**. They describe how to carry out a specific type of analytical task, step by step. A skill file is what you give an LLM agent instead of improvised instructions.

Examples of skills:
- How to investigate a subject (which sources to check, in what order, how to verify)
- How to enrich a piece of evidence (which tools to run, what flags to use, how to interpret the output)
- How to produce a specific type of output (what sections it must contain, what format, what quality gates)
- How to maintain the vault itself (the curation process is itself a skill)

Skill files answer the question: **"how do I do X?"**

### Why the distinction matters for AI

When an LLM agent runs an investigation, it needs both layers. It reads knowledge files to understand the domain context, and it reads skill files to know what steps to execute. If these are mixed together in a single document, the agent cannot distinguish "this is background I should keep in mind" from "this is an instruction I should follow." Keeping them separate makes the agent's behaviour predictable and auditable.

---

## Who is this for?

**Analysts and researchers** in any domain where methodology matters — where the way you do an investigation determines whether the result is reliable. If you have ever finished a complex piece of work, learned something important about how to do it better, and then lost that learning before the next time, this vault architecture solves that problem.

**Teams building agentic AI workflows.** The vault is the instruction layer between a human operator and an LLM. Skill files tell the agent what to do. Prompt files trigger the skill. Workflow files chain skills into pipelines. Session logs close the feedback loop.

**Anyone learning how to work with AI agents effectively.** The single most important factor in LLM output quality is the quality of the instructions it receives. This vault is an architecture for writing those instructions well, maintaining them over time, and improving them from real operational experience.

---

## How the vault works: the full loop

```
30-prompts/          ← you trigger a skill with a prompt
      ↓
10-skills/           ← the skill tells the agent exactly what to do
      ↓
50-knowledge/        ← the skill reads domain context from knowledge files
      ↓
40-workflows/        ← workflows chain multiple skills into pipelines
      ↓
60-sessions/         ← sessions log what happened and flag unexpected findings
      ↓
00-index/lessons-log ← flagged observations accumulate for analyst review
      ↓
10-skills/           ← approved lessons are applied back into skill files
```

Each cycle makes the skill files more accurate. Over time the vault becomes a codification of real operational expertise — not from a single author sitting down to write a manual, but from the gradual accumulation of lessons learned in actual work.

---

## What is in this vault?

### `10-skills/` — How to do things

One file per analytical capability. A skill file is a complete, self-contained procedure: purpose, required inputs, step-by-step method, output format, and notes on edge cases and failure modes.

The key property of a good skill file: **it contains no ambiguity**. An agent reading it knows exactly what to do, in what order, and what a completed run looks like. Vague skill files produce improvised agent behaviour; specific ones produce consistent, auditable results.

**In this vault:** `vault-curation.md` — the skill that governs how the vault itself is maintained over time. `_template.md` — the blank template for adding your own skills.

### `30-prompts/` — How to trigger a skill

A prompt file is the text you use to hand a task to an LLM. It specifies which skill file to read, provides variable placeholders (`{INPUT}`, `{TARGET}`) so the same prompt works across different cases, and defines the expected output format.

A prompt without a skill file behind it is improvised. A prompt that loads a skill file is structured. The difference in output reliability is significant.

**In this vault:** `vault-distillation-prompt.md` — the prompt that triggers a lessons distillation run. `_template.md` — blank template.

### `40-workflows/` — How to chain skills together

When a task requires more than one skill in sequence — for example, gather information, then analyse it, then produce a structured output — a workflow coordinates the phases. Each phase has clear inputs, outputs, and a quality gate before moving to the next.

**In this vault:** `_template.md` — blank template showing the full workflow structure.

### `50-knowledge/` — What you know

Reference material that skills and workflows read from. This is where domain context lives — not how to do things, but what is known about the things you work with.

This vault includes:
- **`ontology-and-llm.md`** — why structured knowledge schemas (ontologies) matter for AI work. The foundational reading for understanding how to make knowledge useful to an LLM rather than decorative.
- **`knowledge-graphs/`** — theory and practice of building graph-structured knowledge bases.
- **`threat-actors/_template.md`** and **`malware-families/_template.md`** — examples of structured entity profiles (these templates apply to any domain where you build profiles of subjects or artefacts).

### `60-sessions/` — What happened

A dated log of every significant piece of work. Sessions serve two purposes: they are the record of what was done, and they are the raw material for vault improvement.

The key feature: a `## Flagged Observations` section where unexpected findings are recorded as *candidates* — not immediately written as lessons. This is deliberate. An LLM working through a session cannot reliably determine root cause, and a finding that seems like a tool failure might be a usage error, an environment issue, or a genuine insight. A human reviews flagged observations in a curation pass and decides which ones become permanent methodology.

**In this vault:** `_template.md` — the session template. Two synthetic examples showing the format.

### `20-llm-configs/` and `22-personas/` — Which AI to use and how

One file per LLM provider or configuration, documenting the endpoint, model, context window, cost tier, and known strengths and weaknesses. Persona files define behavioural contracts for an LLM in a specific role — what you can rely on it to do consistently, and what you should not ask it to do.

### `70-credentials/` — Where secrets live (not what they are)

Masked references and config file paths only. The format records which environment variable to set, which file holds the actual value, and when it was last rotated. The secret itself never enters the vault.

### `97-scripts/` — Code that implements skills

When a skill requires automation, the script that implements it is stored here, linked back to its skill file and workflow. The vault copy is the canonical version; deployed copies on runtime hosts are derived from it.

---

## Ontology: the concept that ties everything together

The `50-knowledge/ontology-and-llm.md` file is worth reading regardless of your domain. It addresses a foundational problem: an LLM has no persistent model of relationships between things. It generates text from statistical patterns. Given a vague question it produces a plausible-sounding answer — which may be wrong.

When you give an LLM a defined schema — what entity types exist, what relationships are allowed between them, what provenance is required on every claim — it can extract structured, verifiable, mergeable information instead of unauditable prose.

The vault's skill files, prompt templates, and workflow runbooks are all applications of the same principle: the more precisely you specify the schema of what the agent should produce, the more reliably it produces it.

---

## Getting started

**In Obsidian:**
Open this directory as an Obsidian vault, install the **Dataview** plugin, and start at `00-index/HOME.md`.

**With Claude Code:**
Open a session in this directory. `CLAUDE.md` loads automatically. Ask the agent to read a skill file and follow it.

**Building your own vault:**
1. Fork this repo
2. Read `10-skills/vault-curation.md` — the maintenance system runs itself once you understand it
3. Copy `10-skills/_template.md` to write your first skill file
4. Log sessions as you work; run a curation pass after every five sessions

---

## Five rules that make it work

| Rule | Why |
|------|-----|
| Knowledge and skills live in separate files | An agent needs to distinguish "context to hold" from "instruction to follow" |
| Skill files are not touched during active work | Editing methodology mid-task creates drift; the curation process exists for a reason |
| Sessions are append-only | Past sessions are the audit trail; add new ones, never edit old ones |
| Observations are flagged, not immediately written as lessons | LLMs cannot reliably diagnose root cause; humans review first |
| Prompts are specific about expected output format | Vague prompts produce improvised outputs; specificity is the defence against hallucination |

---

<img width="1536" height="1024" alt="Knowledge Vault" src="assets/vault-footer.png" />
