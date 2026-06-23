---
title: "Example Workflow — Research Synthesis"
type: workflow
id: wf-example-research-synthesis
volatility: stable
sensitivity: public
tags: [example, research, synthesis, methodology, workflow]
llms: [claude-sonnet, gpt-4o]
status: active
last_updated: 2026-06-23
---

# Example Workflow — Research Synthesis

> **This is a teaching example.** It is intentionally generic and domain-neutral — the
> point is to show how a workflow *chains skills into phases with quality gates*, so you
> can copy the structure for your own work. It contains no sensitive methodology and is
> safe to share. The subject (answering a research question from sources) is the most
> generic analytical task there is, on purpose.

## Purpose

Produce a concise, fully-sourced briefing that answers a research question — by chaining
source collection, source evaluation, and synthesis into three phases, each with a gate
that must pass before the next begins. Invoke it whenever the deliverable is "a defensible
answer with its evidence attached," and you want the *process* to be auditable rather than
a single improvised pass.

This workflow exists primarily as the worked example for [`40-workflows/_template.md`](_template.md):
read it alongside the template to see the structure filled in.

## Prerequisites

- No tools or credentials required (this generic example uses only reading and writing).
- Skill files to read first:
  - [[10-skills/example-source-collection]]
  - [[10-skills/example-source-evaluation]]

## Inputs

| Input | Description | Where to get it |
|-------|-------------|-----------------|
| `{QUESTION}` | One clear sentence stating what must be answered | From the requester |
| `{SCOPE}` | Optional constraints: dates, languages, source types | From the requester |

## Steps

### Phase 1 — Collect

**Goal:** Assemble a complete, traceable set of candidate sources for `{QUESTION}`.

**Actions:**
1. Apply [[10-skills/example-source-collection]] to `{QUESTION}` within `{SCOPE}`.
2. Produce the source table (one row per source, each with a stable `id`).

**Output:** A source table.

**Gate:** Every sub-question of `{QUESTION}` has at least one logged source, or an explicit
"no sources found" note. Do not proceed on a partial set.

---

### Phase 2 — Evaluate

**Goal:** Rate the reliability of each source and the credibility of each key claim.

**Actions:**
1. Apply [[10-skills/example-source-evaluation]] to the Phase 1 table.
2. Produce the claims table with reliability (A–F), credibility (1–6), and a rationale per rating.

**Output:** An evaluated source table + a claims table.

**Gate:** Every key claim the answer will rest on has a rating *with a rationale*, and
single-sourced weak claims are flagged. An unrated claim cannot enter the synthesis.

---

### Phase 3 — Synthesize

**Goal:** Write the briefing, with every assertion traceable to rated evidence.

**Actions:**
1. Answer `{QUESTION}` in 1–3 short paragraphs.
2. Attach to each assertion the supporting source `id`(s) and an overall confidence
   derived from the Phase 2 ratings.
3. List open questions and anything that was single-sourced or unresolved.

**Output:** The final briefing (see Output Format).

**Gate:** No assertion lacks a source reference; confidence reflects the ratings, not optimism.

---

## Output Format

A single Markdown briefing:

```markdown
# Briefing — {QUESTION}

## Answer
<1–3 paragraphs; every assertion ends with [S1, S4] style source refs>

## Confidence
<high | medium | low> — <one line tying this to the Phase 2 ratings>

## Evidence
<the claims table from Phase 2>

## Open questions / weak spots
- <single-sourced claims, gaps, contradictions left unresolved>
```

## Quality Gates

- [ ] Phase 1 gate: all sub-questions covered or explicitly marked empty
- [ ] Phase 2 gate: every key claim rated with a rationale; weak single-sourced claims flagged
- [ ] Phase 3 gate: no unsourced assertion; confidence matches the evidence

## Linked Skills

- [[10-skills/example-source-collection]] — used in Phase 1
- [[10-skills/example-source-evaluation]] — used in Phase 2

## Linked Prompts

- *(none — this example is invoked directly; a prompt file is optional. See `30-prompts/_template.md` to add one.)*

## Notes

- The phases are deliberately separable: collection logs, evaluation judges, synthesis
  concludes. Mixing them is the classic failure mode — an agent that "researches and answers
  in one go" cannot show its work, and you cannot tell a strong conclusion from a confident guess.
- Swap the two skills for your own domain skills and this same three-phase shape (gather →
  assess → produce, with a gate between each) carries over to almost any analytical workflow.
