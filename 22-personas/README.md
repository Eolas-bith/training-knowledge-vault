---
title: "AI Personas — Index"
type: reference
id: persona-personas
volatility: periodic
sensitivity: public
tags: [personas, llm, collaboration, methodology]
status: active
last_updated: 2026-06-02
---

# AI Personas

## What a Persona Is

An AI persona is the behavioral contract layered on top of a raw model. It is distinct from the underlying LLM (tracked in `20-llm-configs/`) and from the model catalog. Where an LLM config describes *what the model can do* (context window, API endpoint, cost), a persona describes *how it presents itself and what you can rely on it to do consistently*.

## Why Personas Matter

**Functional**
A persona provides a stable, predictable interface. You know what behaviors, capabilities, and constraints to expect across sessions regardless of underlying model version changes.

**Epistemic / Trust**
The persona carries trained safety behaviors and refusals that are harder to erode than raw model weights. It signals provenance: output from a named persona carries the alignment posture of its creator, which matters in professional and research contexts.

**Collaborative**
For long-running workflows (session indexing, vault curation, iterative analysis), a named persona with persistent behavioral patterns lets you build methodology *around* it. Skill files, prompt templates, and session rules can be calibrated to how a specific persona behaves. This vault is an example: its skills and workflows are calibrated to the Claude persona.

**Psychological / UX**
Naming and characterising the assistant reduces cognitive load — you don't need to re-negotiate norms each session. It also creates a clear boundary between the tool and the analyst, which matters for analytical hygiene.

---

## Personas Index

| Persona | Provider | Model(s) | Status |
|---------|----------|----------|--------|
| [[22-personas/analyst-operator\|Analyst Operator]] | model-agnostic | — | active |

---

## Notes

- Each persona file documents: purpose, behavioral contract, trust boundaries, and interaction notes.
- Persona files are not model configs — do not duplicate API endpoint or cost data here; link to `20-llm-configs/` instead.
- Add a new persona via `_template.md`.
