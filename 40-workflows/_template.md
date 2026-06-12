---
title: "Workflow Name"
type: workflow
tags: []
llms: []
status: draft
last_updated: YYYY-MM-DD
---

# Workflow Name

## Purpose

One paragraph. What problem does this workflow solve, and when should you invoke it?

## Prerequisites

- Required tools installed and configured
- Required credentials available (see `70-credentials/`)
- Required skill files read (list them)

## Inputs

| Input | Description | Where to get it |
|-------|-------------|----------------|
| `{INPUT_1}` | | |
| `{INPUT_2}` | | |

## Steps

### Phase 1 — [Name]

**Goal:** One sentence.

**Actions:**
1. Step one
2. Step two

**Output:** What Phase 1 produces.

---

### Phase 2 — [Name]

**Goal:** One sentence.

**Actions:**
1. Step one
2. Step two

**Output:** What Phase 2 produces.

---

### Phase 3 — [Name]

**Goal:** One sentence.

**Actions:**
1. Step one
2. Step two

**Output:** What Phase 3 produces.

---

## Output Format

Describe the final deliverable: file format, location, schema.

## Quality Gates

Conditions that must be met before the workflow is considered complete:
- [ ] Gate 1
- [ ] Gate 2

## Linked Skills

- [[10-skills/skill-name]] — used in Phase N
- [[10-skills/skill-name]] — used in Phase N

## Linked Prompts

- [[30-prompts/prompt-name]] — execution trigger for Phase N

## Notes

Edge cases, known failure modes, alternative paths.
