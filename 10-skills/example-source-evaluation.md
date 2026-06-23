---
title: "Example Skill — Source Evaluation"
type: skill
id: skill-example-source-evaluation
volatility: stable
sensitivity: public
tags: [example, research, source-evaluation, credibility, methodology]
llms: [claude-sonnet, gpt-4o]
status: active
last_updated: 2026-06-23
---

# Example Skill — Source Evaluation

> **This is a teaching example.** Generic and domain-neutral by design — a model for
> the *shape* of a skill file, not a sensitive procedure.

## Purpose

Rate each collected source for reliability, and each key claim for credibility, using a
fixed public scale (the Admiralty / NATO source-reliability and information-credibility
system). A fixed scale is the point: it turns a vague "this looks trustworthy" into a
structured, comparable judgement the synthesis step can weight and the reader can audit.
Runs as Phase 2 of the [[40-workflows/example-research-synthesis]] workflow, on the table
produced by [[10-skills/example-source-collection]].

## Compatible LLMs

| LLM | Notes |
|-----|-------|
| claude-sonnet | Good at justifying a rating in one line; hold it to the rubric, not vibes |
| gpt-4o | Equivalent; require the rationale field so a rating can be challenged |

## Required Context / Inputs

- **Source table** — the output of [[10-skills/example-source-collection]] (rows with `id`, locator, type).
- **The key claims** the research question turns on (so credibility is rated where it matters).

## Procedure

1. **Rate each source's reliability** A–F (do not invent intermediate grades):

   | Grade | Meaning |
   |-------|---------|
   | A | Reliable — authoritative, proven track record |
   | B | Usually reliable — minor doubts |
   | C | Fairly reliable |
   | D | Not usually reliable |
   | E | Unreliable |
   | F | Reliability cannot be judged |

2. **Rate each key claim's credibility** 1–6 *independently* of who said it:

   | Grade | Meaning |
   |-------|---------|
   | 1 | Confirmed by independent sources |
   | 2 | Probably true |
   | 3 | Possibly true |
   | 4 | Doubtful |
   | 5 | Improbable |
   | 6 | Truth cannot be judged |

3. **Record a one-line rationale** for every rating. A rating with no rationale is not reusable.
4. **Flag single-sourced key claims** — anything resting on one source that is not graded A1–B2
   is a risk the synthesis must surface, not bury.

## Output Format

Extend the source table with `reliability` (A–F), and add a claims table:

| Claim | Supporting source `id`(s) | Reliability | Credibility | Rationale |
|-------|---------------------------|-------------|-------------|-----------|
| … | S1, S4 | A | 1 | independent confirmation across two primary sources |

## Linked Workflows

- [[40-workflows/example-research-synthesis]] — Phase 2 consumes this skill's output

## Notes

- Reliability (the *source*) and credibility (the *claim*) are rated separately on purpose:
  a reliable source can still carry a doubtful claim, and a weak source can be right.
- This skill **judges**; it does not write the conclusion. That separation is what lets a
  reviewer challenge a rating without re-running the whole investigation.
