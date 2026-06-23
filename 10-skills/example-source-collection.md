---
title: "Example Skill — Source Collection"
type: skill
id: skill-example-source-collection
volatility: stable
sensitivity: public
tags: [example, research, sources, provenance, methodology]
llms: [claude-sonnet, gpt-4o]
status: active
last_updated: 2026-06-23
---

# Example Skill — Source Collection

> **This is a teaching example.** It is deliberately generic and domain-neutral so it
> can be read as a model for writing your own skill files. It carries no sensitive
> methodology. Copy its *shape*, not its subject.

## Purpose

Given a research question, gather candidate sources and log each one with enough
provenance that a later step can evaluate and cite it. The output is a complete,
traceable source set — not an answer. Use this as the first phase of the
[[40-workflows/example-research-synthesis]] workflow, or standalone whenever you
need an auditable list of what a conclusion will rest on.

## Compatible LLMs

| LLM | Notes |
|-----|-------|
| claude-sonnet | Reliable at structured logging; good at de-duplicating near-identical sources |
| gpt-4o | Equivalent; confirm it preserves exact URLs/locators rather than paraphrasing them |

## Required Context / Inputs

- **Research question** — one clear sentence stating what must be answered.
- **Scope constraints** *(optional)* — date range, languages, allowed/excluded source types.

## Procedure

1. **Decompose the question** into 2–5 sub-questions. Collection targets sub-questions,
   not the broad headline — this is what makes the set complete rather than anecdotal.
2. **Search each defined source type** in turn (e.g. primary documents, reference works,
   reporting, datasets). Note the source type as you go.
3. **Log every candidate** in the source table below — one row per source. Capture the
   locator (URL, DOI, file path) *exactly*; do not paraphrase it.
4. **De-duplicate.** Merge rows that are the same source reached two ways; keep the most
   authoritative locator.
5. **Stop at saturation** — when new searches surface only sources already logged, the
   set is complete enough for evaluation.

## Output Format

A Markdown table, one row per source:

| `id` | Title | Author / Publisher | Date | Locator (URL/DOI/path) | Source type | Accessed |
|------|-------|--------------------|------|------------------------|-------------|----------|
| S1 | … | … | YYYY-MM-DD | … | primary / reference / reporting / dataset | YYYY-MM-DD |

The `id` (S1, S2, …) is what downstream phases cite — assign it here and never reuse it.

## Linked Workflows

- [[40-workflows/example-research-synthesis]] — Phase 1 consumes this skill's output

## Notes

- This skill **collects and logs only** — it does not assess quality (that is
  [[10-skills/example-source-evaluation]]) and does not draw conclusions. Keeping those
  steps separate is what makes the chain auditable.
- If a sub-question returns no sources, record that explicitly — an empty result is itself
  a finding the synthesis must account for.
