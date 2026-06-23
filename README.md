<img width="1536" height="1024" alt="Knowledge Vault" src="assets/vault-header.png" />

# Training Knowledge Vault

> A blueprint for structuring analytical knowledge so that both humans and AI can use it reliably.

---

## What is this?

This is a **training version of a structured knowledge vault** — an open blueprint for how to organise methodology and reference knowledge so they can be used by an analyst, an LLM agent, or both working together.

It is not a wiki. It is not a note collection. It is a deliberately structured system where every piece of knowledge has a type, a location, and a clear relationship to the work it supports.

The vault follows one core idea: **if you write your methodology clearly, an AI agent can follow it just as reliably as a human colleague — and improve it over time through a structured feedback loop.**

---

## Why this matters (start here — no technical background needed)

If you only read one section, read this one. It explains *why* a system like this exists before getting into how it is built.

### The problem: a brilliant assistant with no memory and no knowledge of your work

A modern AI model has read an enormous amount of the internet. That makes it a capable generalist — it can write, summarise, and reason about almost any topic. But it has two limitations that matter enormously in real work:

1. **It knows nothing about *your* specific work.** It has never seen how your team does an investigation, what counts as "done" in your field, which sources you trust, or the hard-won lessons you learned the painful way. It only knows the *average* of everything it read.
2. **It does not remember.** Each conversation starts from scratch. Anything you taught it yesterday is gone today unless it was written down somewhere the AI can read.

Think of it as a brilliant new graduate who has read every textbook ever written, starts fresh every morning with no memory of the day before, and — crucially — **never says "I don't know."** When it hits a gap, it fills it with a confident, plausible-sounding guess. In the AI world this is called a *hallucination*. The danger is not that wrong answers look uncertain — it is that **a wrong answer sounds exactly as confident as a right one.**

### The solution: give it the right context, on purpose

**Context** is simply everything the AI knows about the task at the moment it answers. **Context curation** is the deliberate act of deciding what that should be, writing it down clearly, and keeping it current. **Knowledge management** is organising all of it so the *right* piece is in front of the AI at the *right* moment — not buried, not stale, not contradicted by three other notes.

This is the difference between asking a stranger for directions and handing them a map. The stranger improvises; the map-holder follows a known-good route. Curated context is the map.

### A concrete before-and-after

> **Without a vault — raw AI:**
> *"Investigate this company and tell me if it's risky."*
> The AI improvises an answer from its general training. It may invent sources, skip the checks your field considers mandatory, and phrase guesses as facts. Ask twice and you get two different answers. You cannot tell which steps it actually performed.
>
> **With a vault — the AI reads your skill file first:**
> *"Follow the company-investigation skill on this company."*
> Now it works through *your* documented procedure: these sources, in this order, verified this way, with every claim sourced, in the output format your team requires. Run it ten times and you get ten consistent, auditable results — because it is following written methodology, not improvising.

Same model. The only thing that changed is the **quality and structure of the context it was given.** That is the entire premise of this vault.

### How this lets your real expertise actually get used

Most valuable knowledge in any organisation is *tacit* — it lives in experienced people's heads and in scattered notes, and it evaporates when they are busy, on holiday, or gone. An AI cannot use knowledge it cannot see.

Curating that expertise into structured, written form does three things:

- **It makes hidden know-how explicit and reusable.** Your best practice, written down once, can be applied every time — by a junior colleague, by you next year, or by an AI agent — without depending on the original expert being in the room.
- **It makes the AI apply *your* standards, not the internet's average.** A well-written knowledge base steers the model toward how *your domain* does things, instead of a bland blend of everything it ever read.
- **It compounds instead of evaporating.** Because every piece of work can feed a lesson back into the written knowledge (the "feedback loop" below), the system gets *more* accurate the more it is used — the opposite of notes that rot in a drawer.

In one line: **un-curated context in → confident nonsense out; curated context in → reliable, auditable work out.** Everything else in this README is the machinery for doing that curation well and keeping it honest over time.

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

**With an AI coding/agent tool:**
The instructions are tool-neutral and live in **`AGENTS.md`**, with thin adapters so each tool loads them automatically. Open a session in this directory and ask the agent to read a skill file and follow it.

| Tool | What loads automatically |
|------|--------------------------|
| **Codex** (OpenAI) | `AGENTS.md` |
| **Google Antigravity** | `AGENTS.md` + `GEMINI.md` |
| **Gemini CLI** | `AGENTS.md` + `GEMINI.md` (via `.gemini/settings.json`) |
| **Claude Code** | `CLAUDE.md`, which imports `AGENTS.md` |
| **Ollama / LM Studio** and other local runners | none — load `AGENTS.md` as the system prompt manually (see `AGENTS.md` → *Using this vault with any AI tool*) |

Edit `AGENTS.md` to change the instructions; the adapter files (`CLAUDE.md`, `GEMINI.md`) point back to it, so there is no second copy to keep in sync.

**Building your own vault:**
1. Fork this repo
2. Read `10-skills/vault-curation.md` — the maintenance system runs itself once you understand it
3. Copy `10-skills/_template.md` to write your first skill file
4. Log sessions as you work; run a curation pass after every five sessions

---

## The rules that make it work

| Rule | Why |
|------|-----|
| Knowledge and skills live in separate files | An agent needs to distinguish "context to hold" from "instruction to follow" |
| Skill files are not touched during active work | Editing methodology mid-task creates drift; the curation process exists for a reason |
| Sessions are append-only | Past sessions are the audit trail; add new ones, never edit old ones |
| Observations are flagged, not immediately written as lessons | LLMs cannot reliably diagnose root cause; humans review first |
| Prompts are specific about expected output format | Vague prompts produce improvised outputs; specificity is the defence against hallucination |
| Identity is decoupled from path (`id`) | Append-only sessions hard-code locations; stable ids let the structure be reorganised without breaking the audit trail |
| Structure is enforced, not just documented | `vault-doctor.py` + a pre-commit hook + CI guarantee invariants regardless of how carefully anyone behaves |

---

## Enforced invariants: structure you don't have to remember

Process discipline (how you and your agent *should* behave) degrades silently as a
vault grows: a file gets created without frontmatter, a new directory never makes it
into the routing table, a moved file leaves broken links behind, a private note ends
up referenced from a public one. The fix is to make the structure *self-checking* so
those failures surface as build errors instead of latent rot.

Three additions carry this:

- **`id` — stable identity, decoupled from path.** Every file has a permanent slug
  that never changes even when the file moves. Cross-references from append-only
  material (sessions, the investigations index) record the `id`, not the path — so the
  knowledge tree can be reorganised freely without rewriting history. This directly
  resolves the tension between "sessions are immutable" and "knowledge should be
  reorganisable."

- **`volatility` and `sensitivity` — classification that drives placement and access.**
  `volatility` (`stable | periodic | volatile`) says how often a file changes and is the
  antidote to the "knowledge becomes a junk drawer" failure mode: separate by how often
  things change, not just by topic. `sensitivity` (`public | internal | private`) makes
  the privacy boundary machine-checkable rather than a hopeful instruction.

- **`97-scripts/vault-doctor.py` — the enforcement layer.** A dependency-free checker
  for frontmatter, enum conformance, id uniqueness, navigation parity (every section is
  routed in the canonical instructions file, `AGENTS.md`), link integrity, and the rule that a `public` file may never
  link to a `private` one. It runs in a pre-commit hook and in CI (`--strict`). The
  canonical field definitions live in `00-index/frontmatter-schema.md`.

The guiding idea: **encode each structural lesson as a check, not just a paragraph.**
A rule you have to remember will eventually be forgotten; a rule the build enforces
cannot be.

---

## Plain-language glossary

The rest of this vault uses a few recurring terms. If any were unfamiliar above, here they are in plain English:

| Term | In plain language |
|------|-------------------|
| **LLM** (Large Language Model) | The AI engine itself — e.g. Claude, GPT, Gemini, or a model you run on your own computer. It predicts text; on its own it has no memory of you and no knowledge of your specific work. |
| **Agent** | An LLM that has been given tools and instructions so it can actually *do* tasks (read files, run steps), not just chat. |
| **Context** | Everything the AI can "see" at the moment it answers — your question plus whatever files and instructions were loaded. Good answers depend far more on good context than on a cleverer model. |
| **Context window** | The size limit on how much context fits at once, measured in *tokens*. Like short-term memory: there is only so much room, so you load what matters. |
| **Token** | The unit the AI counts text in — very roughly ¾ of a word. Everything loaded into context costs tokens, which is why the always-loaded instruction file is kept lean. |
| **Prompt** | The instruction you give the AI to start a task. A good prompt points it at the right skill file rather than relying on it to improvise. |
| **Hallucination** | A confident, plausible-sounding answer that is simply wrong — what the AI produces when it has to fill a gap it has no real information for. Curated context is the main defence. |
| **Curation** | The ongoing work of deciding what knowledge to keep, writing it clearly, fixing what is wrong, and removing what is stale — so the AI is always working from a trustworthy, current source. |
| **Ontology** | A clear map of the *types of things* in your field and how they relate (e.g. a "threat actor" *uses* a "malware family"). Giving the AI this map lets it produce structured, checkable answers instead of loose prose. See `50-knowledge/ontology-and-llm.md`. |
| **Skill file** | A written, step-by-step procedure for one kind of task — the AI's instruction manual for doing it your way, every time. |
| **Knowledge file** | Reference material *about* your domain — facts and background the AI reads to understand the subject, separate from the step-by-step instructions. |
| **Session log** | A dated record of a piece of work: what was done and anything surprising that came up, kept so lessons can be reviewed and folded back in later. |
| **Agent context file** | The instruction file a tool auto-loads at the start of a session — `AGENTS.md` here, with `CLAUDE.md`/`GEMINI.md` as thin adapters pointing to it. |

---

<img width="1536" height="1024" alt="Knowledge Vault" src="assets/vault-footer.png" />
